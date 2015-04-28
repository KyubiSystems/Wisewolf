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

# Save categories to DB
for c in o.categories:
    cat = Category.create(name = c)
    cat.save()

# Save feeds to DB
for f in o.feeds:

    print '------------'
    print f

    cat_id = Category.get(Category.name == f['category']).id    

    if o.version == "1.0":
        # Add feed from OPML version 1.0
        feed = Feed.create(name = f['text'], category = cat_id, version = f['type'], url = f['url'])
    elif o.version == "1.1":
        # Add feed from OPML version 1.1
        feed = Feed.create(name = f['title'], category = cat_id, version = f['type'], comment = f['text'], url = f['xmlUrl'])
    else:
        continue

    # Add feed to DB
    feed.save()
