#!/usr/bin/env python
"""
OPML reader for Wisewolf RSS
(c) 2015 KyubiSystems: www.kyubi.co.uk
"""
import xml.etree.ElementTree as ET

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

    def __init__(self, filename):
        self.filename = filename
        self.attribs = {}
        self.categories = []
        self.links = []

    def parseOpml(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()

        # Use XPath to parse header files
        
        for xpath in ['title', 'dateCreated', 'dateModified', 'ownerName', 'ownerEmail', 'link']:
            self.attribs[xpath] = root.find('./head/'+xpath)

        # Parse body items
        for child in root.iter('outline'):
            if 'url' not in child.attrib.keys():
                self.categories.append(child.attrib['text'])
                print "\nCategory: "+child.attrib['text']
            else:
                print "\nLink:\n-----"
                for (key, value) in child.attrib.iteritems():
                    print key+": "+value

