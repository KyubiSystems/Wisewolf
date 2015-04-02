#!/usr/bin/env python
"""
Testing OPML import
(c) 2015 KyubiSystems: www.kyubi.co.uk
"""
from opml import Opml

#o = Opml.OpmlReader('./opml/testing.xml')
o = Opml.OpmlReader('./opml/opml-example.xml')

o.parseOpml()

# Show retrieved data structures
print o.categories
print o.feeds
