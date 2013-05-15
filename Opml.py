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

for child in root.iter('outline'):
    print child.tag, child.attrib

