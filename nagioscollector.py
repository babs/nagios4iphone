#!/usr/bin/python

import urllib2, urllib, re, urlparse, ConfigParser
from pprint import pprint
from Nagios import *

import __builtin__


def main():
	conf = ConfigParser.ConfigParser({'version':"3"})
	conf.read( "nagioscollector.ini" )
	serverpool = NagiosServers()
	for s in conf.sections():
		if conf.has_option(s, 'active') and conf.get(s, 'active') == "1":
			serverpool.register(
				s,
				conf.get(s, 'host'),
				conf.get(s, 'username'),
				conf.get(s, 'password'),
				realm          = conf.get(s, 'realm'),
				nagios_version = conf.get(s, 'version')
				)
	serverpool.update()
	pprint(serverpool.overall_status())
	
if __name__ == "__main__":
	main()
