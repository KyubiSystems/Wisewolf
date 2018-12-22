#!/usr/bin/env python
"""
Testing OPML import
(c) 2015 KyubiSystems: www.kyubi.co.uk
"""
from opml import Opml
from models import Category, Feed, IntegrityError

o = Opml.OpmlReader('./opml/testing.xml')

o.parseOpml()

# Show retrieved data structures
print(o.version)

# Save categories to DB, skip invalid or duplicate feeds
for c in o.categories:
    cat = Category.create(name=c)
    try:
        cat.save()
    except IntegrityError:
        pass

# Iterate over feeds found
for f in o.feeds:

    print('------------')
    print(f)

    # Get corresponding Category id
    cat_id = Category.get(Category.name == f['category']).id    

    if o.version == "1.0":
        # Add feed from OPML version 1.0
        feed = Feed.create(name=f['text'], category=cat_id, version=f['type'], url=f['url'])
    elif o.version == "1.1" or o.version == "2.0":
        # Add feed from OPML version 1.1
        feed = Feed.create(name=f['title'], category=cat_id, version=f['type'], comment=f['text'],
                           description=f['description'], url=f['xmlUrl'])
    else:
        continue

    # Add feed to DB, skip invalid or duplicate feeds
    try:
        feed.save()
    except IntegrityError:
        pass
