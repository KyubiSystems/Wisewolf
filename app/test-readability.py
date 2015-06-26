#!/usr/bin/env python

from readability.readability import Document
import urllib

url = "http://hosted2.ap.org/APDEFAULT/cae69a7523db45408eeb2b3a98c0c9c5/Article_2015-06-25-ML-Islamic-State/id-c6a64e8323414ec1bc9c7a95a2a31455"

html = urllib.urlopen(url).read()
readable_article = Document(html).summary()
readable_title = Document(html).short_title()

print readable_title

print readable_article
