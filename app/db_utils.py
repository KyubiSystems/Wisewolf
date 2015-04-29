#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2015 Kyubi Systems: www.kyubi.co.uk
"""
from models import *
from urlparse import urlparse
import urllib2

import logging
log = logging.getLogger('wisewolf.log')

# Create SQLite3 tables
def create_db():

    # Define database
    db = SqliteDatabase(DB_FILE, threadlocals=True)

    # Connect to database
    db.connect()

    # Create tables
    Category.create_table()
    Feed.create_table()
    Post.create_table()
    Image.create_table()


# load default feeds in DB
# Start with defaults file in PSV
# Consider moving to OPML later?
def load_defaults():

    # Open defaults file
    with open(DEFAULTS_FILE, 'r') as f:
        rows = f.readlines()
    f.close()

    # Define database
    db = SqliteDatabase(DB_FILE, threadlocals=True)

    # Connect to database
    db.connect()

    # Iterate over default feeds list
    # PSV format name|url|category
    for row in rows:
        (name, url, category) = row.split('|')
        category = category.strip()
        # Update Category table
        c = Category.create(name=category, comment='default category')
        # Get Category insert id
        cid = c.id
        # Update Feeds table
        f = Feed.create(name=name, version='', url=url, category=cid, favicon='', comment='default feed')
        # Get Feed insert id
        fid = f.id
        # Get favicon for this Feed
        # returns path to local favicon file, or None
        # write to current feed record
        favicon = get_favicon(fid)
        if favicon:
            f.favicon = favicon
            f.save()


# Get favicon file for server
# and write to cache directory
def get_favicon(id):

    feed = Feed.get(Feed.id == id)
    url = feed.url
    u = urlparse(url)
    favicon_url = 'http://' + u.netloc + '/favicon.ico'
    try:
        f = urllib2.urlopen(favicon_url)
    except urllib2.HTTPError:
        return None

    log.info("Favicon {0} status: {1}".format(str(id), str(f.getcode()))) 
    favicon_data = f.read()
    favicon_path = '{0}favicon_{1}.ico'.format(ICONS_PATH, str(id)) # Full filepath to favicon
    favicon_file = 'favicon_{1}.ico'.format(str(id)) # favicon filename

    with open(favicon_path, 'wb') as fav:
        fav.write(favicon_data)
    fav.close()

    # Return filename of favicon
    return favicon_file

# TODO: Delete favicon from cache when corresponding feed deleted from DB.








