#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from models import *
from db_utils import create_db, load_defaults
import multiprocessing
import datetime
import requests

# Server startup options
# --quiet: no printed output
# --nows: no websocket output, just update DB


def site_is_up(url):
    state = False
    r = requests.head(url)
    if r.status_code == 200:
        state = True
    return state


def worker(wid):
    """Thread worker function"""
    print "Starting reader process  ", wid

    # Define database
    db = SqliteDatabase(DB_FILE)

    # Connect to database
    db.connect()

    wfeed = Feed.get(Feed.id == wid)
    print "URL: ", wfeed.url

    # Check RSS URL up, skip to next refresh if not
    # Can implement exponential backoff later
    # 2^n multiple on refresh time, up to limit, then disable?

    if site_is_up(wfeed.url):
        print "Yes, site is up!"

    # Grab RSS posts using feedparser

    # Filter for new posts since last check

    # Check for posts IN DA FUTURE!!
    now = datetime.datetime.now()

    # Filter text for dangerous content (eg. XSRF?)

    # Wait for write lock on DB

    # Add to database

    # Release write lock on DB

    # Spawn websocket message with new posts for web client
    # Define error codes for feed not responding etc.

    # Wait for next refresh
    # Refresh = 0 means exit now

    db.close()

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






