$ = function (id) { return document.getElementById(id);};
spbi = window.iui.showPageById;
function loadDatas(aValue) {
	$('target').innerHTML=aValue;
}
var NagiosDatas = "";
addEventListener("load", function(event) {
var req = new XMLHttpRequest();
req.onreadystatechange = function() {
	if (this.readyState == 4) {
		NagiosDatas = json_parse(this.responseText);
		collect_and_update();
		for (e in NagiosDatas) {
			var a = document.createElement("a")
			a.innerHTML=e;
			a.setAttribute('onclick','loadNagiosServer("'+e+'")');
			a.setAttribute('href','#shownagiosserver');
			var li = document.createElement("li");
			var span = document.createElement('span');
			var stats = getserverstats(e);
			span.appendChild(document.createTextNode(
				sprintf(" (T:%d O:%d W:%d C:%d)", stats['TOTAL'], stats['OK'], stats['WARNING'], stats['CRITICAL'])
			));
			//
			span.style.fontSize = "10pt";
			a.appendChild(span)
			li.appendChild(a);
			$('overall_list').appendChild(li);
		}
	}
}
req.open("GET", "datas.json", true);
// Sample
//req.open("GET", "js/datas.json", true);
req.send(null);
}, false);

loadNagiosServer = function (server) {
	collect_and_update(server);
	$('ov_sname').innerHTML = server + " overview"
	var o = $('shownagiosserver');
	o.setAttribute('title',server);
	var dest_list = $('shownagiosserver_ul');
	dest_list.innerHTML = "";
	var e = server;
	for ( f in NagiosDatas[e] ) {
		var sli = document.createElement("li");
		sli.appendChild(document.createTextNode(f+":"));
		var container = document.createElement('div');
		
		container.style.marginLeft = "10px";
		container.className = "service_listing";
		for ( g in NagiosDatas[e][f] ) {
			if ( NagiosDatas[e][f][g]["status"] == "OK" ) continue;
			var service = document.createElement("div");
			
			service.appendChild(document.createTextNode(
				g + ": "
			));
			var st = document.createElement('span');
			st.className = NagiosDatas[e][f][g]["status"];
			st.appendChild( document.createTextNode(NagiosDatas[e][f][g]["status"]));
			service.appendChild(st);
			service.appendChild(document.createElement('br'));
			service.appendChild(document.createTextNode(
				NagiosDatas[e][f][g]["message"]
			));
			container.appendChild( document.createElement('br') );

			var a = document.createElement('a');
			a.appendChild(service);
			a.setAttribute('href',"javascript:update_service_detail('"+e+"','"+f+"','"+g+"');spbi('service_detail')");
			a.className = "arrow";
			container.appendChild(a);

			//container.appendChild(service);
		}
		if ( container.childNodes.length == 0 ) continue;
		sli.appendChild(container);
		dest_list.appendChild(sli);
	}
}

update_service_detail = function (nagiosserver, server, service) {
	var s = NagiosDatas[nagiosserver][server][service];
	var dest = $('service_detail');
	dest.setAttribute('title',sprintf('%s on %s',service, server));

	flushNode(dest);
	var ul = document.createElement('ul');
	
	var li = document.createElement('li');
	li.appendChild(document.createTextNode(
		sprintf("Server: %s", server)
	));
	ul.appendChild(li);

	var li = document.createElement('li');
	li.appendChild(document.createTextNode(
		sprintf("Monitored by: %s", nagiosserver)
	));
	ul.appendChild(li);

	var li = document.createElement('li');
	li.appendChild(document.createTextNode(
		sprintf("Service: %s", service)
	));
	ul.appendChild(li);
	
	var li = document.createElement('li');
	li.appendChild(document.createTextNode(
		sprintf("Status: %s", s['status'])
	));
	ul.appendChild(li);
	
	var li = document.createElement('li');
	li.appendChild(document.createTextNode(
		sprintf("Since: %s", s['duration'])
	));
	ul.appendChild(li);
	
	var li = document.createElement('li');
	li.appendChild(document.createTextNode(
		sprintf("Attempts: %s", s['attempts'])
	));
	ul.appendChild(li);

	var li = document.createElement('li');
	li.appendChild(document.createTextNode(
		sprintf("Message: %s", s['message'])
	));
	ul.appendChild(li);
	
	var li = document.createElement('li');
	li.appendChild(document.createTextNode(
		sprintf("Last checked on: %s", s['lastcheck'])
	));
	ul.appendChild(li);
	
	dest.appendChild(ul);
}

show_allerrors = function () {
	var dest_list = $('allerrors_ul');
	dest_list.innerHTML = "";
	for ( e in NagiosDatas ) {
		for ( f in NagiosDatas[e] ) {
			for ( g in NagiosDatas[e][f] ) {
				if ( NagiosDatas[e][f][g]["status"] == "OK" ) continue;
				var li = document.createElement("li");
				li.innerHTML = g+"<br/>"+
					NagiosDatas[e][f][g]["status"] + "<br/>" +
					NagiosDatas[e][f][g]["message"];
				dest_list.appendChild(li);
			}
		}
	}

}


getserverstats = function (srv) {
	var r = {'TOTAL':0, 'OK':0, 'WARNING':0, 'CRITICAL':0};
	var e = srv;
	for ( f in NagiosDatas[e] ) {
		for ( g in NagiosDatas[e][f] ) {
			var st = NagiosDatas[e][f][g].status;
			if ( r[st] ) {
				r[st] += 1;
			} else {
				r[st] = 1;
			}
			r['TOTAL'] += 1;
		}
	}
	return r;

}

collect_and_update = function (srv) {
	var r = {'TOTAL':0, 'OK':0, 'WARNING':0, 'CRITICAL':0};
	if (srv) {
		r = getserverstats(srv)
	} else {
		for ( e in NagiosDatas ) {
			var srvstats = getserverstats(e);
			for ( f in srvstats) {
				if ( r[f] ) {
					r[f] += srvstats[f];
				} else {
					r[f] = srvstats[f];
				}
			}
		}
	}
	var postname = "";
	if ( srv ) {
		postname = "srv";
	}
	for (e in r) {
		var elem = $(e+'qty'+ postname);
		if ( elem ) {
			flushNode(elem);
			elem.appendChild(document.createTextNode(r[e] + " (" + Math.round((r[e]*100)/r['TOTAL']) + "%)"));
		}
	}
	try {
		var OK = Math.round((r['OK']*100)/r['TOTAL']);
		$('OKbar'+ postname).style.width       = OK+'%';
	
		var WARNING = Math.round((r['WARNING']*100)/r['TOTAL']);
		$('WARNINGbar'+ postname).style.width  = WARNING+'%';
	
		var CRITICAL = Math.round((r['CRITICAL']*100)/r['TOTAL']);
		$('CRITICALbar'+ postname).style.width = CRITICAL+'%';
	
	} catch (e) {}
	//alert();
}

flushNode = function (node) {
	if ( node.hasChildNodes() ) {
		while ( node.childNodes.length >= 1 ) {
			node.removeChild( node.firstChild );       
		} 
	}
}
