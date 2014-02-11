#!/usr/bin/python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
---
feedtest: Test lightweight feed autodiscovery

Usage:
TBD. Modify for internal unit testing?
"""

import feedfind
import urllib

p = feedfind.FeedFind()

f = urllib.urlopen("http://www.slashdot.org")
html = f.read()
p.feed(html)

print p.feeds
p.close()
