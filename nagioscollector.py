#!/usr/bin/python

import urllib2, urllib, re, urlparse, ConfigParser
from pprint import pprint

RE_Status  = re.compile("'status(OK|WARNING|CRITICAL)'")
RE_Message = re.compile("<TD CLASS='status[^']+'(?: valign='center'| nowrap)?>(.*?)</TD>")


from htmlentitydefs import name2codepoint as n2cp
def substitute_entity(match):
	ent = match.group(2)
	if match.group(1) == "#":
		return unichr(int(ent))
	else:
		cp = n2cp.get(ent)
		if cp:
			return unichr(cp)
		else:
			return match.group()

def decode_htmlentities(string):
	entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
	return entity_re.subn(substitute_entity, string)[0]

def fetch_status(nagios_host, username, password, realm='Nagios Access', nagios_version=3):
	if int(nagios_version) == 3:
		nagios_loc = "cgi-bin/nagios3/"
	else:
		nagios_loc = "nagios/cgi-bin/"

	nagios_base = urlparse.urljoin(nagios_host, nagios_loc)
	# print nagios_base
	pwdman = urllib2.HTTPBasicAuthHandler()
	pwdman.add_password(realm, nagios_base, username, password)
	opener = urllib2.build_opener(pwdman)
	urllib2.install_opener(opener)
	datas = urllib2.urlopen(nagios_base+'status.cgi?host=all').read()
	server_and_services = filter(
		lambda x: 'extinfo.cgi?type=2&host=' in x,
		datas.split('extinfo.cgi?type=1&host=')
		)

	services_status = {}
	for serverel in server_and_services:
		server = serverel.split("'",1)[0]
		services = serverel.split("extinfo.cgi?type=2&host=%s&service="%server )[1:]
		for service in services:
			if not "</TR></TABLE></TD>" in service: continue
			# print "-"*50
			# print service
			# print "-"*50
			sname = urllib.unquote_plus(service.split("'",1)[0])
			s = services_status.setdefault(server,{}).setdefault(sname, {})
			s['name']   = urllib.unquote_plus(sname)
			msgst = RE_Message.findall(service)
			if len(msgst) == 5:
				s['status']    = decode_htmlentities(msgst[0]).strip()
				s['lastcheck'] = decode_htmlentities(msgst[1]).strip()
				s['duration']  = decode_htmlentities(msgst[2]).strip()
				s['attempts']  = decode_htmlentities(msgst[3]).strip()
				s['message']   = decode_htmlentities(msgst[4]).strip()
	return services_status

def main():
	conf = ConfigParser.ConfigParser({'version':"3"})
	conf.read( "nagioscollector.ini" )
	AllStatus = {}
	for s in conf.sections():
		if conf.has_option(s, 'active') and conf.get(s, 'active') == "1":
			try:
				AllStatus[s] = fetch_status(
					conf.get(s, 'host'),
					conf.get(s, 'username'),
					conf.get(s, 'password'),
					realm          = conf.get(s, 'realm'),
					nagios_version = conf.get(s, 'version')
					)
			except Exception as e:
				print "Error while fetching %s -> %s"%(conf.get(s, 'host'),str(e))
	pprint(AllStatus)
	# fetch_status("https://minnie.neolane.net/","nagiosadmin","NeoNagiosAdmin",nagios_version=3)
	# fetch_status("https://mickey.neolane.net/","nagiosadmin","NeoNagiosAdmin",nagios_version=3)
	# fetch_status("https://pipil.us.neolane.net/","nagiosadmin","NeoNagiosAdmin",nagios_version=2)
	# fetch_status("https://hoagie.neolane.org/","nagiosadmin","NeoNagiosAdmin",nagios_version=3)
	
if __name__ == "__main__":
	main()
