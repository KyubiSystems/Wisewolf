#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from models import *
from db_utils import create_db, load_defaults

print "Starting Wisewolf server v0.02..."

# Check for existence of SQLite3 database, creating if necessary
if not os.path.exists(DB_FILE):
    print "SQLite database not found, creating...",
    create_db()
    print " done."

# Check whether Feeds table is empty
# Populate from default entries

print "Checking number of feeds: ",
numberFeeds = fn.Count(Feed.id)
print numberFeeds+" found"

if numberFeeds == 0:
    print "Loading default entries...",
    load_defaults()
    print " done."


