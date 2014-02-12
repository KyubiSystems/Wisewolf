#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from models import *
from db_utils import create_db, load_defaults
import feedparser
import argparse


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

    # Check ETag, Modified: Attempt Conditional HTTP retrieval
    # to reduce excessive polling
    if hasattr(wfeed, 'etag'):
        d = feedparser.parse(wfeed.url, etag=wfeed.etag)
    elif hasattr(wfeed, 'last_modified'):
        d = feedparser.parse(wfeed.url, modified=wfeed.last_modified)
    else:
        d = feedparser.parse(wfeed.url)

    if d.status < 400:
        # Site appears to be up
        print "Site "+wfeed.url+" is up, status: "+str(d.status)
        # Reset error counter
        Feed.update(errors=0).where(Feed.id == wid)

        prefiltered=False

        # Get RSS/ATOM version number
        print "Version: "+d.version

        # Catch 301 Moved Permanently, update feed address
        if d.status == 301:
            Feed.update(url=d.href).where(Feed.id == wid)

        # Conditional HTTP:
        # Check for ETag in result and write to DB
        if hasattr(d, 'etag'):
            print "ETag "+d.etag
            Feed.update(etag=d.etag).where(Feed.id == wid)
            prefiltered=True

        # Conditional HTTP
        # Check for Last-Modified in result and write to DB
        if hasattr(d, 'modified'):
            print "Modified "+d.modified
            Feed.update(last_modified=d.modified).where(Feed.id == wid)
            prefiltered=True

        # Check for feed modification date, write to DB
        if hasattr(d, 'published'):
            print "Published: "+d.published

        if hasattr(d, 'updated'):
            print "Updated: "+d.updated

        # If entries exist, process them
        if d.entries:

            # If we haven't already date filtered, do it now
            if not prefiltered:
                pass

            # Iterate over posts found
            # Need to check difference between RSS and ATOM
            for post in d.entries:
                print post.get('title', 'No title')
                print post.get('description', 'No description')
                print post.get('published', datetime.datetime.now())  # should use feed updated date?
                print post.get('content', 'No content')
                print post.get('link', 'No link')
                print '------------'

            # Filter text for dangerous content (eg. XSRF?)
            # Feedparser already does this to some extent

            # Wait for write lock on DB

            # Add to database

            # Release write lock on DB

            # Spawn websocket message with new posts for web client
            # One WS message per feed or one per post?

            # Define error codes for feed not responding etc.

            print "================"

    else:
        # Site appears to be down
        print "Site "+wfeed.url+" is down, status: "+str(d.status)

        # Increment error counter
        Feed.update(errors=Feed.errors + 1).where(Feed.id == wid)

        # Status 410 Gone Permanently, mark feed inactive
        if d.status == 410:
            Feed.update(inactive=True).where(Feed.id == wid)
            return

        # Implement exponential in case feed is down
        # 2^n multiple on refresh time, up to limit, then disable?

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

    # Get list of active Feed ids from database
    feed_query = Feed.select().where(Feed.inactive == 0)
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
        print "Loading default entries..."
        load_defaults()
        print "Loading default entries done."

    return


if __name__ == '__main__':

    # Server startup options
    # --quiet: no printed output
    # --nows: no websocket output, just update DB

    parser = argparse.ArgumentParser(description="Wisewolf RSS server process")
    parser.add_argument("--quiet", help="Suppress terminal output")
    parser.add_argument("--nows", help="No websocket messaging, just update DB")
    args = parser.parse_args()

    # print startup message, create DB if necessary
    startup()

    # Run RSS request processes in parallel
    rss_parallel()







