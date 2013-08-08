#!/usr/bin/python

"""feedtest: Test lightweight feed autodiscovery

Usage:
	TBD. Modify for internal unit testing?
"""

import feedfind, urllib

p = feedfind.FeedFind()

f = urllib.urlopen("http://www.slashdot.org")
html = f.read()
p.feed(html)

print p.feeds
p.close()
