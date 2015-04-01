#!/usr/bin/env python
"""
OPML reader for Wisewolf RSS
(c) 2015 KyubiSystems: www.kyubi.co.uk
"""
import xml.etree.ElementTree as ET
import urllib

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

    def __init__(self, filename, check=True):
        self.filename = filename
        self.attribs = {}
        self.categories = []
        self.links = []
        self.check = check

    def parseOpml(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()

        # Get OPML version number
#        version = tree.find('./opml').attrib['version']
        v = root.attrib['version']
        print "OPML version " + v
        if v == "1.0":
            url = "url"
        elif v == "1.1":
            url = "xmlUrl"
        else: 
            print "Unrecognised OPML version:", v
            raise

        # Use XPath to parse header files
        
        for xpath in ['title', 'dateCreated', 'dateModified', 'ownerName', 'ownerEmail', 'link']:
            self.attribs[xpath] = root.find('./head/'+xpath)

        # Parse body items
        for child in root.iter('outline'):
            if url not in child.attrib.keys():
                self.categories.append(child.attrib['text'])
                print "\nCategory: "+child.attrib['text']
            else:
                print "\nLink:\n-----"
                for (key, value) in child.attrib.iteritems():
                    print key+": "+value

                # Check if feed url exists, get HTTP response code              
                if self.check == True:
                    try:
                        a = urllib.urlopen(child.attrib[url])
                    except IOError:
                        print "ERROR: Host unreachable"
                    else:
                        print "Response: " + str(a.getcode())





