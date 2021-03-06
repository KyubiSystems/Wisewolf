"""
Wisewolf RSS Reader
(c) 2015 Kyubi Systems: www.kyubi.co.uk
---
autodiscovery: Find the RSS/ATOM feed(s) for a given web page

Usage:
feed(uri) - returns feed found for a URI
"""

try:
    from html.parser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

# Declare valid RSS and ATOM feed types for autodetection

FEED_TYPES = ('application/rss+xml',
              'text/xml',
              'application/atom+xml',
              'application/x.atom+xml',
              'application/x-atom+xml')

# Define feed discovery class

class Discover(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.feeds = [] # list of returned feed (title,URL) tuples

    # Search for <LINK> tag in header

    def handle_starttag(self, tag, attr):
        if tag != 'link':
            return

        attributes = dict(attr) # convert name-value tuples to dict
        if 'type' not in attributes:
            return

        if attributes['type'] not in FEED_TYPES:
            return

        if 'title' in attributes:
            title = attributes['title']
        else:
            title = 'None'

        link = attributes['href']
        fulluri = self.makeFullURI(link)

        self.feeds.append({'title' : title, 'fulluri' : fulluri})

    # Convert partial to full URIs

    def makeFullURI(self, uri):
        uri = uri.strip()
        if uri.startswith('feed://'):
            uri = uri.replace('feed://', 'http://', 1)
        for x in ['http', 'https']:
            if uri.startswith('%s://' % x):
                return uri
            return 'http://%s' % uri
