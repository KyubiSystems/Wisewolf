#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from models import *
from db_utils import create_db, load_defaults
import feedparser

# Server startup options
# --quiet: no printed output
# --nows: no websocket output, just update DB


def rss_worker(wid):
    """RSS gevent worker function"""
    print "Starting reader process ", wid

    # Set Feedparser User-Agent string defined in config
    feedparser.USER_AGENT = USER_AGENT

    # Define database
    db = SqliteDatabase(DB_FILE)

    # Connect to database, get URL
    db.connect()
    wfeed = Feed.get(Feed.id == wid)

    # Attempt RSS retrieval, check HTTP status
    d = feedparser.parse(wfeed.url)

    if d.status < 400:
        # Site appears to be up
        print "Site "+wfeed.url+" is up, status: "+str(d.status)

        # Get ETag and Last-Modified values to reduce excessive polling
        try:
            print "Etag "+d.etag
        except AttributeError:
            pass

        try:
            print "Modified "+d.modified
        except AttributeError:
            pass

        if d.entries:
            print "Found entry:", d.entries[0]

        # Catch redirect if Status 301, update RSS address in database

    else:
        # Site appears to be down
        print "Site "+wfeed.url+" is down, status: "+str(d.status)

        # Implement exponential in case feed is down
        # Mark feed inactive if Status 410
        # 2^n multiple on refresh time, up to limit, then disable?

        # If server doesn't implement Last-Modified,
        # filter for new posts since last check

    # Filter text for dangerous content (eg. XSRF?)

    # Wait for write lock on DB

    # Add to database

    # Release write lock on DB

    # Spawn websocket message with new posts for web client
    # One WS per feed or one per post?

    # Define error codes for feed not responding etc.

    # Wait for next refresh
    # Refresh = 0 means exit now

    db.close()

    return


# RSS gevent parallel server process
def rss_parallel():
    import gevent.monkey
    gevent.monkey.patch_all()
    from gevent.pool import Pool

    # Set limit of 10 simultaneous requests
    pool = Pool(10)

    # Get list of Feed ids from database
    feed_query = Feed.select()
    feed_ids = [f.id for f in feed_query]

    # Add Feed id to Gevent worker pool
    for feed_id in feed_ids:
        pool.spawn(rss_worker, feed_id)
    pool.join()


# Startup message, DB creation check, load default feeds
def startup():

    print "Starting Wisewolf server v0.02a..."

    # Check for existence of SQLite3 database, creating if necessary
    if not os.path.exists(DB_FILE):
        print "SQLite database not found, creating...",
        create_db()
        print "done."

    # Checking number of feeds
    print "Checking number of feeds: ",
    number_feeds = Feed.select().count()
    print "{} found".format(number_feeds)

    # Load defaults in database if blank
    if number_feeds == 0:
        print "Loading default entries...",
        load_defaults()
        print "done."

    return


if __name__ == '__main__':

    # print startup message, create DB if necessary
    startup()

    # Run RSS request processes in parallel
    rss_parallel()







