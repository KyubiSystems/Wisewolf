#!/usr/bin/env python
"""
OPML reader for Wisewolf RSS
(c) 2015 KyubiSystems: www.kyubi.co.uk
"""
import xml.etree.ElementTree as ET
import urllib
import logging as log

class OpmlReader:
    """
    Parses standard OPML export files, adds them to database
    """

    def __repr__(self):
        return "<OpmlReader object: %s>" % self.attribs['title']

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "<OpmlReader object: %s>" % self.attribs['title']

    def __init__(self, filename, check=True, verbose=True):
        self.filename = filename
        self.attribs = {}
        self.categories = []
        self.feeds = {}
        self.check = check
        if verbose:
            log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        else:
            log.basicConfig(format="%(levelname)s: %(message)s")

    def parseOpml(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()

        # Get OPML version number
#        version = tree.find('./opml').attrib['version']
        v = root.attrib['version']
        log.info("OPML version " + v)
        if v == "1.0":
            url = "url"
        elif v == "1.1":
            url = "xmlUrl"
        else: 
            log.error("Unrecognised OPML version:", v)
            raise

        # Use XPath to parse header files
        
        for xpath in ['title', 'dateCreated', 'dateModified', 'ownerName', 'ownerEmail', 'link']:
            self.attribs[xpath] = root.find('./head/'+xpath)

        # Parse body items
        for child in root.iter('outline'):
            if url not in child.attrib.keys():
                category = child.attrib['text']
                self.categories.append(category)
                log.info("New category found: "+category)

            else:
                log.info("New feed found")
                feed = {}
                for (key, value) in child.attrib.iteritems():
                    log.info(key+": "+value)
                    feed[key] = value
                    feed['category'] = self.categories[-1]

                # Check if feed url exists, get HTTP response code              
                if self.check:
                    try:
                        a = urllib.urlopen(feed[url])
                    except IOError:
                        log.warn("Host unreachable, skipped: " + feed[url])
                    else:
                        status = str(a.getcode())
                        log.info("Response: " + status)
                        feed['status'] = status
                        self.feeds.append(feed)

                else:
                    feed['status'] = None
                    self.feeds.append(feed)





