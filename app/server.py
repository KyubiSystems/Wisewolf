#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from models import *
from db_utils import create_db, load_defaults
import feedparser
import argparse

# Set up gevent multithreading
import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool

# Set up server logging
import logging
logging.basicConfig(level=logging.INFO,
                    filename='wisewolf.log', # log to this file
                    format='%(asctime)s %(levelname)s: %(message)s') # include timestamp, level

def rss_worker(wid):
    """RSS gevent worker function"""
    logging.info("Starting reader process %s", wid)

    # Set Feedparser User-Agent string defined in config
    feedparser.USER_AGENT = USER_AGENT

    # Define database
    db = SqliteDatabase(DB_FILE, threadlocals=True)

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
        logging.info("Site %s is up, status: %s", wfeed.url, str(d.status))

        # Reset error counter
        Feed.update(errors=0).where(Feed.id == wid)

        prefiltered=False

        # Get RSS/ATOM version number
        logging.info("Feed version: %s", d.version)

        # Catch 301 Moved Permanently, update feed address
        if d.status == 301:
            Feed.update(url=d.href).where(Feed.id == wid)

        # Conditional HTTP:
        # Check for ETag in result and write to DB
        if hasattr(d, 'etag'):
            logging.info("Etag %s", d.etag)
            Feed.update(etag=d.etag).where(Feed.id == wid)
            prefiltered=True

        # Conditional HTTP
        # Check for Last-Modified in result and write to DB
        if hasattr(d, 'modified'):
            logging.info("Modified %s", d.modified)
            Feed.update(last_modified=d.modified).where(Feed.id == wid)
            prefiltered=True

        # Check for feed modification date, write to DB
        if hasattr(d, 'published'):
            logging.info("Published: %s", d.published)

        if hasattr(d, 'updated'):
            logging.info("Updated: %s", d.updated)

        # If entries exist, process them
        if d.entries:

            # If we haven't already date filtered, do it now
            if not prefiltered:
                pass

            # Iterate over posts found
            # Build and add Post object to DB
            for post in d.entries:
                p = Post()
                p.title = post.get('title', 'No title')
                p.description = post.get('description', 'No description')
                p.published = post.get('published', datetime.datetime.now())  # should use feed updated date?
                p.content = post.get('content', 'No content')
                p.link = post.get('link', 'No link')
                p.feed = wid
                p.save()

            # Filter text for dangerous content (eg. XSRF?)
            # Feedparser already does this to some extent

            # If strip_images set
            # Get image links from content and add to DB
            # Tagged by feed and post ID

            # Wait for write lock on DB

            # Add to database

            # Release write lock on DB

            # Spawn websocket message with new posts for web client
            # One WS message per feed or one per post?

            # Define error codes for feed not responding etc.

    else:
        # Site appears to be down
        logging.warning("Site %s is down, status: %s", wfeed.url, str(d.status))

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

    logging.info("Starting Wisewolf server v0.02a...")

    # Check for existence of SQLite3 database, creating if necessary
    if not os.path.exists(DB_FILE):
        logging.info("SQLite database not found, creating...")
        create_db()
        logging.info("done.")

    # Checking number of feeds
    logging.info("Checking number of feeds: ")
    number_feeds = Feed.select().count()
    logging.info("%d found", number_feeds)

    # Load defaults in database if blank
    if number_feeds == 0:
        logging.info("Loading default entries...")
        load_defaults()
        logging.info("Loading default entries done.")

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







