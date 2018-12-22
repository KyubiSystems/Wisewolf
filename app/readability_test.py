#!/usr/bin/env python

import urllib.request, urllib.parse, urllib.error
import sys

from readability.readability import Document

url = sys.argv[1]

#url = "http://www.space.com/29740-mice-of-mars-rodents-pave-way-to-red-planet.html"

html = urllib.request.urlopen(url).read()
readable_article = Document(html).summary()
readable_title = Document(html).short_title()

print(readable_title)

print(readable_article.encode('utf-8').strip())
