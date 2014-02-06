#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from models import *
from db_utils import create_db, load_defaults
import multiprocessing

# Server startup options
# --quiet: no printed output
# --nows: no websocket output, just update DB

def worker(wid):
    """Thread worker function"""

    # Check RSS URL up, skip to next refresh if not
    # Can implement exponential backoff later

    # Grab RSS posts using feedreader

    # Filter for new posts since last check

    # Filter text for dangerous content (eg. XSRF?)

    # Wait for write lock on DB

    # Add to database

    # Release write lock on DB

    # Spawn websocket message with new posts for web client
    # Define error codes for feed not responding etc.

    # Wait for next refresh
    # Refresh = 0 means exit now

    print "Worker: ", wid
    return

if __name__ == '__main__':

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
    # Select all Feeds, get Feed ids, start worker process by id

    feed_q = Feed.select()
    idFeeds = [f.id for f in feed_q]
    jobs = []
    for i in idFeeds:
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()






