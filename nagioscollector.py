#!/usr/bin/python

import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import urllib2, urllib, re, urlparse, ConfigParser, json
from pprint import pprint
from Nagios import *
from bottle import route, PasteServer, response, request, run, send_file

import __builtin__


@route('/')
def static_index():
	return send_file("index.html", root=os.path.join(ROOT, './static/'))

@route('/js/:filename#.*#')
def static_js(filename):
	return send_file(filename, root=os.path.join(ROOT, './static/js/'))

@route('/imgs/:filename')
def static_imgs(filename):
	return send_file(filename, root=os.path.join(ROOT, './static/imgs/'))

@route('/css/:filename')
def static_css(filename):
	return send_file(filename, root=os.path.join(ROOT, './static/css/'))

@route('/iui/:filename')
def static_iui(filename):
	return send_file(filename, root=os.path.join(ROOT, './static/iui/'))

@route('/datas.json')
def generate_json():
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
	#pprint(serverpool.overall_status())
	#pprint(serverpool.as_dict())
	return json.dumps(serverpool.as_dict())

def main():
	run(host="0.0.0.0")
	
if __name__ == "__main__":
	# Interractive launch
	main()
else:
	# Mod WSGI launch
	os.chdir(ROOT)
	application = default_app()

