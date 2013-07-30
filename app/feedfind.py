"""feedfind: Find the RSS/ATOM feed for a given web page

Usage:
	feed(uri) - returns feed found for a URI
"""

import urllib, urlparse, re, sys, HTMLParser

class FeedFind(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attributes):
        if tag != 'a' : return


def makeFullURI(uri):
    uri = uri.strip()
    if uri.startswith('feed://'):
        uri = uri.replace('feed://','http://',1)
    for x in ['http','https']:
        if uri.startswith('%s://' % x):
            return uri
    return 'http://%s' % uri

def isFeedLink(link):
    return link[-4:].lower() in ('.rss', '.rdf', '.xml', '.atom')
