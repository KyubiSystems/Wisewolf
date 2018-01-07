#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2017 Kyubi Systems: www.kyubi.co.uk
"""

import logging
from config import DB_FILE, DEFAULTS_FILE
from models import Category, Feed, Post, Image, SqliteDatabase
from imgcache.Imgcache import getFavicon

# Set up logging
log = logging.getLogger('wisewolf.log')

# Create SQLite3 tables
def create_db():

    logging.info("Creating SQLite database %s..." % DB_FILE)

    # Define database
    db = SqliteDatabase(DB_FILE, threadlocals=True)

    # Connect to database
    db.connect()

    # Create tables
    Category.create_table()
    Feed.create_table()
    Post.create_table()
    Image.create_table()

    # Create default Unsorted category
    Category.create(name='Unsorted', comment='Uncategorised feeds', order=1)

    logging.info("Database created.")

# load default feeds in DB
# Start with defaults file in PSV
# Consider moving to OPML later?
def load_defaults():

    logging.info("Loading default feed entries into database %s..." % DB_FILE)

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
        c = Category.create(name=category, comment='Default category', order=1)
        # Get Category insert id
        cid = c.id
        # Update Feeds table
        f = Feed.create(name=name, version='', url=url, category=cid, favicon='', comment='Default feed', description='Default feed')
        # Get Feed insert id
        fid = f.id
        # Get favicon for this Feed
        # returns path to local favicon file, or None
        # write to current feed record
        logging.info("Getting favicon for %s" % f.url)
        f.favicon = getFavicon(fid)
        logging.info("Got favicon %s" % f.favicon)

        # Save entry to feeds table
        f.save()

    logging.info("Default feeds loaded.")








