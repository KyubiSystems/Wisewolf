#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""
from models import *


# Create SQLite3 tables
def create_db():

    # Define database
    db = SqliteDatabase(DB_FILE)

    # Connect to database
    db.connect()

    # Create tables
    Category.create_table()
    Feed.create_table()
    Post.create_table()


# load default feeds in DB
# Start with defaults file in PSV
# Consider moving to OPML later?
def load_defaults():
    print "Starting defaults loader...",

    # Open defaults file
    with open(DEFAULTS_FILE, 'r') as f:
        rows = f.readlines()
    f.close()

    # Define database
    db = SqliteDatabase(DB_FILE)

    # Connect to database
    db.connect()

    # Iterate over default feeds list
    # PSV format name|url|category
    for row in rows:
        (name, url, category) = row.split('|')
        # Update Category table
        c = Category()
        c.name = category
        c.save()
        # Get Category insert id
        cid = c.id
        # Update Feeds table
        Feed.create(name=name, url=url, category=cid)

    print "done"


