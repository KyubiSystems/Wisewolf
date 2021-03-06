#!/usr/bin/env python
"""
OPML reader for Wisewolf RSS
(c) 2015 KyubiSystems: www.kyubi.co.uk
"""
import xml.etree.ElementTree as ET
import urllib.request, urllib.parse, urllib.error
import logging as log

class OpmlReader:
    """
    Parses standard OPML export files, adds them to database
    """

    def __repr__(self):
        return "<OpmlReader object: %s>" % self.attribs['title']

    def __str__(self):
        return str(self).encode('utf-8')

    def __unicode__(self):
        return "<OpmlReader object: %s>" % self.attribs['title']

    def __init__(self, filename, check=True, verbose=False):
        self.filename = filename
        self.attribs = {}
        self.categories = ['Unsorted'] # Add default 'Unsorted' category
        self.feeds = []
        self.check = check
        self.version = None  # OPML version number
        if verbose:
            log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        else:
            log.basicConfig(format="%(levelname)s: %(message)s")

    def parseOpml(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()

        # Get OPML version number
        v = root.attrib['version']
        self.version = v
        log.info("OPML version " + v)
        if v == "1.0":
            url = "url"
        elif v == "1.1" or v == "2.0":
            url = "xmlUrl"
        else: 
            log.error("Unrecognised OPML version:", v)
            raise

        # Use XPath to parse header files
        
        for xpath in ['title', 'dateCreated', 'dateModified', 'ownerName', 'ownerEmail', 'link']:
            self.attribs[xpath] = root.find('./head/'+xpath)

        # Parse body items
        for child in root.iter('outline'):
            if url not in list(child.attrib.keys()):
                category = child.attrib['text']
                self.categories.append(category)
                log.info("New category found: "+category)

            else:
                log.info("New feed found")
                feed = {}
                for (key, value) in child.attrib.items():
                    log.info(key+": "+value)
                    feed[key] = value

                # If categories defined, allocate last category found to feed
                # TODO: Do this consistently via tree parent
                if self.categories[-1]:
                    feed['category'] = self.categories[-1]
                else:
                    feed['category'] = 'Unsorted'
                        
                # Check if feed url exists, get HTTP response code              
                if self.check:
                    try:
                        a = urllib.request.urlopen(feed[url])
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





