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
loging.basicConfig(level=logging.INFO,
                   filename='wisewolf.log', # log to this file
                   format='%(asctime)s %(levelname)s: %(message)s') # include timestamp, level

# Set Feedparser User-Agent string defined in config
feedparser.USER_AGENT = USER_AGENT

# Define database
db = SqliteDatabase(DB_FILE, threadlocals=True)

# --------------------------------------------------
# RSS gevent parallel server process
def rss_server():

    c = Count() # initialise loop interval counter at 1
    
    # Set limit of 10 simultaneous RSS requests
    pool = Pool(10)

    # check feed intervals in DB
    # get feeds which match current tick

    # Get list of active Feed ids from database
    feed_query = Feed.select().where(Feed.inactive == 0)

    # loop over feeds found, spawn rss_worker(id, url)
    # pass row object to worker directly?

    for f in feed_query:
        pool.spawn(rss_worker, f)
    pool.join()

    # send websocket message with updated Feed IDs

    # increment Tick
    c.increment()

    # wait $REFRESH minutes

# --------------------------------------------------
# spawn Worker(feed)
def rss_worker(f):
    """RSS gevent worker function"""
    logging.info("Starting reader process for feed %s", f.id)

    # Check ETag, Modified: Attempt Conditional HTTP retrieval
    # to reduce excessive polling
    if hasattr(f, 'etag'):
        d = feedparser.parse(f.url, etag=f.etag)
    elif hasattr(f, 'last_modified'):
        d = feedparser.parse(f.url, modified=f.last_modified)
    else:
        d = feedparser.parse(f.url)

    # Check returned HTTP status code
    if d.status < 400:
        # Site appears to be UP
        logging.info("Site %s is UP, status %s", f.url, str(d.status))

        # Reset error counter
        if f.errors > 0:
            Feed.update(errors=0).where(Feed.id == f.id)

        prefiltered=False

        # Get RSS/ATOM version number
        logging.info("Feed version: %s", d.version)

        # Catch status 301 Moved Permanently, update feed address
        if d.status == 301:
            Feed.update(url=d.href).where(Feed.id == f.id)

        # Conditional HTTP:
        # Check for Etag in result and write to DB
        if hasattr(d, 'etag'):
            logging.info("Etag %s", d.etag)
            Feed.update(etag=d.etag).where(Feed.id=f.id)
            prefiltered=True




# filter for new items since last check (timedelta)

# wait for write lock on DB

# write Posts items to DB

# update Feed last checked

# release write lock

# return new items Y/N code

# ------

# --------------------------------------------------
# Startup message, DB creation check, load default feeds
def startup():

    logging.info("Starting Wisewolf server version v0.03...")

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
        logging.info("Loading default entries done")

    return

# --------------------------------------------------
# interval counter class

class Count:
    def __init__(self):
        self.counter = 1
    def get(self):
        return self.counter
    def increment(self):
        self.counter += 1
        if self.counter > 96:
            self.counter = 1

# --------------------------------------------------

if __name__ == '__main__':

    # Server startup options
    # --nows: no websocket output, just update DB

    parser = argparse.ArgumentParser(description="Wisewolf RSS server process")
    parser.add_argument("--nows", help="No websocket output, just update DB")
    args = parser.parse_args()

    # print startup message, create DB if necessary
    startup()

    # Start main RSS server loop
    rss_server()
