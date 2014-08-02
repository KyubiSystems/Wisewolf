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
import gevent
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

# Set default reload interval to 15 minutes
INTERVAL = 900

# Define database
db = SqliteDatabase(DB_FILE, threadlocals=True)

# --------------------------------------------------
# RSS gevent parallel server process
def rss_server():
    
    # Set limit of 10 simultaneous RSS requests
    pool = Pool(10)

    # Get list of active Feed ids from database
    feed_query = Feed.select().where(Feed.inactive == 0)

    # loop over feeds found, spawn rss_worker(feed)

    for f in feed_query:
        pool.spawn(rss_worker, f)
    pool.join()

def rss_server_loop():

    c = Count() # initialise loop interval counter at 1

    while True:
        # check feed intervals in DB
        # get feeds which match current tick
        counter = c.get()

        logging.info("Interval tick %d", counter)

        # Call RSS server to spawn another query set
        rss_server()

        # wait INTERVAL seconds
        gevent.sleep(INTERVAL)

        # increment tick
        c.increment()

# --------------------------------------------------
# spawn Worker(feed)
def rss_worker(f):
    """RSS gevent worker function"""
    logging.info("Starting reader process for feed %s", f.id)

    # Connect to database
    db.connect()

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
            logging.info("Etag: %s", d.etag)
            Feed.update(etag=d.etag).where(Feed.id=f.id)
            prefiltered=True

        # Conditional HTTP
        # Check for Last-Modified in result and write to DB
        if hasattr(d, 'modified'):
            logging.info("Modified %s", d.modified)
            Feed.update(last_modified=d.modified).where(Feed.id == f.id)
            prefiltered=True

        # Check for feed modification date, write to DB
        if hasattr(d, 'published'):
            logging.info("Published: %s", d.published)

        if hasattr(d, 'updated'):
            logging.info("Updated: %s", d.updated)

        # If post entries exist, process them
        if d.entries:

            # If we haven't already date filtered, do it now
            # filter for new items since last check (timedelta)
            if not prefiltered:
                pass

            # Iterate over posts found
            # Build and add Post object to DB
            # DB write lock needed?
            for post in d.entries:
                p = Post()
                p.title = post.get('title', 'No title')
                p.description = post.get('description', 'No description')
                p.published = post.get('published', datetime.datetime.now()) # should use feed updated date?
                p.content = post.get('content', 'No content')
                p.link = post.get('link', 'No link')
                p.feed = f.id
                p.save() # Save Post data to DB

            # Filter text for dangerous content (e.g. XSRF?)
            # Feedparser already does this to some extent

            # update Feed last checked date

            # Spawn websocket message with new posts for web client

    else: 
        # Site appears to be down
        logging.warning("Site %s is DOWN, status: %d", f.url, d.status)

        # Increment error counter
        Feed.update(errors = Feed.errors + 1).where(Feed.id == f.id)
        
        # Status 410 Gone Permanently, mark feed inactive
        if d.status == 410:
            Feed.update(inactive==True).where(Feed.id == f.id)

        # Spawn websocket message reporting error to web client

    # Disconnect from database
    db.close()

    return


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
# rolls over at 96

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
    gevent.Greenlet.spawn(rss_server_loop)
