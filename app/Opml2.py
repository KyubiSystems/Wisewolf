#!/usr/bin/env python

"""
(c) 2013 -- KyubiSystems

OPML reader for Wisewolf RSS
"""
import xml.etree.ElementTree as ET

class OpmlReader():
    """
    Parses standard OPML export files, adds them to database
    """

    def __repr__(self):
        return "<OpmlReader object: %s>" % self.attribs['title']

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "<OpmlReader object: %s>" % self.attribs['title']

    def __init__(self):
        self.attribs = {}
        self.categories = []
        self.links = []
        self.filename = ""

    def setOpmlFile(self, filename):
        self.filename = filename

    def parseOpml(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()

        # Use XPath to parse header files
        
        for xpath in ['title', 'dateCreated', 'dateModified', 'ownerName', 'ownerEmail', 'link']:
            self.attribs[xpath] = root.find(xpath)

        # Parse body items
        for child in root.iter('outline'):
            if 'url' not in child.attrib.keys():
                print "\nCategory: "+child.attrib['text']
            else:
                print "\nLink:\n-----"
                for (key, value) in child.attrib.iteritems():
                    print key+": "+value

