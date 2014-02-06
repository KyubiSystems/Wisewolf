#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from models import *
from db_utils import create_db, load_defaults

# Server startup options
# --quiet: no printed output
# --nows: no websocket output, just update DB

print "Starting Wisewolf server v0.02..."

# Check for existence of SQLite3 database, creating if necessary
if not os.path.exists(DB_FILE):
    print "SQLite database not found, creating...",
    create_db()
    print "done."

# Check whether Feeds table is empty
# Populate from default entries

print "Checking number of feeds: ",
numberFeeds = Feed.select().count()
print "{} found".format(numberFeeds)

if numberFeeds == 0:
    print "Loading default entries...",
    load_defaults()
    print "done."
    numberFeeds = Feed.select().count()

# Start multiprocess RSS requests in background, one per feed
# Grab RSS posts using feedreader
# Filter for new posts, add to database
# Spawn websocket message with new posts



