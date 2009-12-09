#!/usr/bin/python

import re, urllib, urllib2, urlparse
from datetime import datetime

RE_Status  = re.compile("'status(OK|WARNING|CRITICAL)'")
RE_Message = re.compile("<TD CLASS='status[^']+'(?: valign='center'| nowrap)?>(.*?)</TD>")
entity_re  = re.compile("&(#?)(\d{1,5}|\w{1,8});")

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
	return entity_re.subn(substitute_entity, string)[0]

class NagiosServers:
	def __init__(self):
		self.nagiosservers = {}
	
	def register(self, name, nagios_host, username, password, realm='Nagios Access', nagios_version=3, fetch=0):
		self.nagiosservers[name] = NagiosServer(name, nagios_host, username, password, realm, nagios_version, fetch)
		
	def update(self):
		for e in self.nagiosservers:
			self.nagiosservers[e].fetch()

	def overall_status(self):
		st = {}
		for nserver in self.nagiosservers:
			nserver_status = self.nagiosservers[nserver].overall_status()
			for k in nserver_status:
				if st.has_key(k):
					st[k] += nserver_status[k]
				else:
					st[k] =  nserver_status[k]
		return st


class NagiosServer:
	def __init__(self, name, nagios_host, username, password, realm='Nagios Access', nagios_version=3, fetch=0):
		self.servername     = name
		self.host           = nagios_host
		self.username       = username
		self.password       = password
		self.realm          = realm
		self.nagios_version = nagios_version
		self.servers        = []
		self.lastfetch      = None
		if fetch:
			self.fetch()

	def fetch(self):
		self.lastfetch = datetime.now()
		self.servers = []
		if int(self.nagios_version) == 3:
			nagios_loc = "cgi-bin/nagios3/"
		else:
			nagios_loc = "nagios/cgi-bin/"
	
		nagios_base = urlparse.urljoin(self.host, nagios_loc)
		pwdman = urllib2.HTTPBasicAuthHandler()
		pwdman.add_password(self.realm, nagios_base, self.username, self.password)
		opener = urllib2.build_opener(pwdman)
		urllib2.install_opener(opener)
		datas = urllib2.urlopen(nagios_base+'status.cgi?host=all').read()
		servers = filter(
			lambda x: 'extinfo.cgi?type=2&host=' in x,
			datas.split('extinfo.cgi?type=1&host=')
			)
		for serverdatas in servers:
			self.servers.append(Server(serverdatas))

	def __repr__(self):
		return "<%s instance for %s>"%(self.__class__, self.servername)
		
	def overall_status(self):
		st = {}
		for server in self.servers:
			server_status = server.overall_status()
			for k in server_status:
				if st.has_key(k):
					st[k] += server_status[k]
				else:
					st[k] =  server_status[k]
		return st


class Server:
	def __init__(self, datas = None):
		self.servername = ""
		self.services   = []
		if datas:
			self.parse(datas)

	def parse(self, datas):
		self.servername = datas.split("'",1)[0]
		services = datas.split("extinfo.cgi?type=2&host=%s&service="%self.servername )[1:]
		for servicedata in services:
			if not "</TR></TABLE></TD>" in servicedata: continue
			self.services.append(Service(servicedata))
	
	def __repr__(self):
		return "<%s instance for %s>"%(self.__class__, self.servername)
	
	def overall_status(self):
		st = {}
		for service in self.services:
			if st.has_key(service.status):
				st[service.status] += 1
			else:
				st[service.status] = 1
		return st

class Service:
	def __init__(self, datas = None):
		self.servicename = ""
		self.status      = ""
		self.atempts     = ""
		self.duration    = ""
		self.message     = ""
		self.lastcheck   = ""
		if datas:
			self.parse(datas)

	def parse(self, datas):
		sname = urllib.unquote_plus(datas.split("'",1)[0])
		self.servicename = urllib.unquote_plus(sname)
		msgst = RE_Message.findall(datas)
		if len(msgst) == 5:
			self.status    = decode_htmlentities(msgst[0]).strip()
			self.lastcheck = decode_htmlentities(msgst[1]).strip()
			self.duration  = decode_htmlentities(msgst[2]).strip()
			self.attempts  = decode_htmlentities(msgst[3]).strip()
			self.message   = decode_htmlentities(msgst[4]).strip()

	def __repr__(self):
		return "<%s instance for %s>"%(self.__class__, self.servicename)
