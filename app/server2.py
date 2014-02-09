#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from models import *
from db_utils import create_db, load_defaults
import datetime
import httplib
import feedparser
from urlparse import urlparse

# Server startup options
# --quiet: no printed output
# --nows: no websocket output, just update DB


def site_is_up(url):
    p = urlparse(url)
    conn = httplib.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400


def rss_worker(wid):
    """RSS gevent worker function"""
    print "Starting reader process ", wid

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
        print "Yes, site is up! ", wid

        # Grab RSS posts using feedparser
        d = feedparser.parse(wfeed.url)
        if d.entries:
            print 'Found entry:', d.entries[0]

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







