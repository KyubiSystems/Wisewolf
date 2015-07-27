#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
---
feedtest: Test lightweight feed autodiscovery

Usage:
TBD. Modify for internal unit testing?
"""

import autodiscovery
import urllib
import requests

url = 'http://www.slashdot.org'
r = requests.get(url)

print r.headers['content-type']

p = autodiscovery.Discover()

f = urllib.urlopen(url)
html = f.read()
p.feed(html)

print p.feeds
p.close()
