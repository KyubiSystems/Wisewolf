#!/usr/bin/env python

"""
Opml -- v 0.01

(c) 2013 -- KyubiSystems

OPML reader for Wisewolf RSS
"""

import xml.etree.ElementTree as ET

filename = "opml-example.xml"

tree = ET.parse(filename)

root = tree.getroot()

# Use XPath to parse header items
title = root.find("./head/title")
print title.text

dateCreated = root.find("./head/dateCreated")
print dateCreated.text

dateModified = root.find("./head/dateModified")
print dateModified.text

ownerName = root.find("./head/ownerName")
print ownerName.text

ownerEmail = root.find("./head/ownerEmail")
print ownerEmail.text

opmlLink = root.find("./head/link")
print opmlLink.text

print '-------------'

# Parse body items
for child in root.iter('outline'):
    if 'url' not in child.attrib.keys():
        print "\nCategory: "+child.attrib['text']
    else:
        print "\nLink:\n-----"
        for (key, value) in child.attrib.iteritems():
            print key+": "+value

