"""feedfind: Find the RSS/ATOM feed for a given web page

Usage:
	feed(uri) - returns feed found for a URI
"""

import urllib, urlparse, re, sys, HTMLParser

# Declare valid RSS and ATOM feed types for autodetection

FEED_TYPES = ('application/rss+xml',
              'text/xml',
              'application/atom+xml',
              'application/x.atom+xml',
              'application/x-atom+xml')

# Define feed finder class

class FeedFind(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.data = [] # list of returned feed URLs
        self.title = [] # list of returned feed titles

# Search for <LINK> tag in header

    def handle_starttag(self, tag, attr):
        if tag != 'link' : return
        attributes = dict(attr) # convert name-value tuples to dict
        if attributes['type'] not in FEED_TYPES : return
        if isFeedLink(attributes['href']):
            if 'title' in attributes:
                self.title.append(attributes['title'])
            else:
                self.title.append('None')
                                
            link = attributes['href']
            fulluri = makeFullURI(value)
            self.data.append(fulluri)

# Convert partial to full URIs

def makeFullURI(uri):
    uri = uri.strip()
    if uri.startswith('feed://'):
        uri = uri.replace('feed://','http://',1)
    for x in ['http','https']:
        if uri.startswith('%s://' % x):
            return uri
    return 'http://%s' % uri

# Check for feed link extension

def isFeedLink(link):
    return link[-4:].lower() in ('.rss', '.rdf', '.xml', 'atom')
