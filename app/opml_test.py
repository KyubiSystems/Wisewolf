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

# Save categories to DB, skip invalid or duplicate feeds
for c in o.categories:
    cat = Category.create(name = c)
    try:
        cat.save()
    except IntegrityError:
        pass

# Save feeds to DB, skip invalid or duplicate feeds
for f in o.feeds:
    # TODO: Check OPML version here, branch on o.version when creating feed
    # Find more OPML examples!
    feed = Feed.create(name = f.title, category = f.category, version = f.type, comment = f.text, url = f.xmlUrl)
    try:
        feed.save()
    except IntegrityError:
        pass
