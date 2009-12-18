Nagios 4 iPhone
===============

A Nagios interface for iPhone without touching anything on your nagios servers.



This software is in two parts:

 * A server side collector and generator which collects statistics on several [nagios][nagios] servers, serve few static files and generate a JSON (using [bottle][bottle])
 * A client side using [iui][iui] and some JS to handle the display

[nagios]: http://www.nagios.org/
[bottle]: http://bottle.paws.de/
[iui]: http://code.google.com/p/iui/

Requirements  
------------

All you need is the simplejson package available on Debian using "apt-get install python-simplejson".

If you fetches N4I via git, you'll need to init and update the bottle submodule:

<pre>
$ git submodule init
Submodule 'bottle' (git://github.com/babs/bottle.git) registered for path 'bottle'
$ git submodule update
Initialized empty Git repository in &lt;where you checked out N4I&gt;/bottle/.git/
remote: Counting objects: 1126, done.
remote: Compressing objects: 100% (468/468), done.
remote: Total 1126 (delta 686), reused 1044 (delta 636)
Receiving objects: 100% (1126/1126), 1.13 MiB | 658 KiB/s, done.
Resolving deltas: 100% (686/686), done.
Submodule path 'bottle': checked out '66ccf95229e41db8e236e86e77b86bb6aea84c24'
</pre>


Configuration
-------------

Copy the nagioscollector.sample.ini to nagioscollector.ini and edit it to fit your needs.

[DEFAULT] values will be used if not overrided in other sections.

Each following sections will become a server.

### Server configuration directives ###

 * username: the username to use to go through Nagios authentication
 * password: do I realy need to explain ?
 * version:  the Nagios version of the server (links slightly change between versions)
 * realm:    Authentication realm proposed for nagios authentication (default: Nagios Access)
 * host:     Url used to access the server hosting nagios without the nagios path, ex: https://my.nagios.server/
 * active:   Set it to 1 to enable collection of this server.

Server side
-----------

There is two way to get the collector running:

 * Standalone mode:

   Just run nagioscollector.py, it will listen on every interfaces on port 8080, then just point your browser to http://<your-server>:8080/, and enjoy.
 * Apache embeded:

   In order to get nagioscollector running in apache, you'll need mod_wsgi installed and properly configured.
Example:
<pre>
    WSGIDaemonProcess N4I user=www-data group=www-data processes=1 threads=5
    WSGIProcessGroup N4I
</pre>

   And you'll need to alias the script to a specified path (in any/all virtualhost you'd like to use it):
<pre>
WSGIScriptAlias /n4i &lt;where you cloned N4I&gt;/nagioscollector.py
</pre>

   Use you're favourite web browser to go to http://<your-server>/n4i/ and enjoy.

Client side
-----------

Use the iPhone browser to go on your freshly deployed N4I and touch the + symbol, then select "Add to Home Screen".

N.B.: Every time you load the application (or use the Reload button), it will take some time to collect all Nagios datas and send the JSON to your iPhone. Please, be patient, it can be a bit long, depending of how many servers and how many services are monitored. For 650+ services across 5 nagios servers, it takes around 7 seconds to load over a medium-high latency network.

Licence (MIT)
=============
    Copyright (c) 2009, Damien Degois.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

