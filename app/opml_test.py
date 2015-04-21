#!/usr/bin/env python
"""
Testing OPML import
(c) 2015 KyubiSystems: www.kyubi.co.uk
"""
from opml import Opml
from models import *

o = Opml.OpmlReader('./opml/testing.xml')
#o = Opml.OpmlReader('./opml/opml-example.xml')

o.parseOpml()

# Show retrieved data structures
print o.version
print o.categories
print o.feeds

# Save categories to DB
for c in o.categories:
    cat = Category.create(name = c)
    cat.save()

# Save feeds to DB
for f in o.feeds:
    # Check OPML version here?
    feed = Feed.create(name = f.title, category = f.category, version = f.type, comment = f.text, url = f.xmlUrl)
    feed.save()
