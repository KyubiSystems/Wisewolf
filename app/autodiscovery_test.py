#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
---
feedtest: Test lightweight feed autodiscovery

Usage:
TBD. Modify for internal unit testing?
"""

import sys
import autodiscovery
import requests

# Declare valid RSS and ATOM feed types for autodetection

FEED_TYPES = ('application/rss+xml',
              'text/xml',
              'application/atom+xml',
              'application/x.atom+xml',
              'application/x-atom+xml')

url = 'http://www.slashdot.org'

# Retrieve target URL
r = requests.get(url)

if (r.status_code != requests.codes.ok):
    print('Request error')
    sys.exit(1)

# Get Content-Type
contenttype = r.headers['content-type']
print(contenttype)

# If Content-Type is RSS feed, return
if (contenttype in FEED_TYPES):
    print('RSS feed detected ' + url)
    sys.exit(0)

# If Content-Type is HTML, pass to autodiscovery
if (contenttype == 'text/html'):

    p = autodiscovery.Discover()

    p.feed(r.text)

    print(p.feeds)
    p.close()
    
    sys.exit(0)
