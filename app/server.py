#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2015 Kyubi Systems: www.kyubi.co.uk
"""

# import system libraries
import feedparser
import argparse
import os

# import Wisewolf libraries
from config import *
from models import *
from imgcache.Imgcache import getFavicon
from db.DatabaseUtils import *

# Set up gevent multithreading
import gevent
import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool

# Set up server logging
import logging
logging.basicConfig(level=logging.INFO,
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
# Default rss_spawn() will check all feeds in DB
def rss_spawn(tick=1):

    # Connect to database
    db.connect()
    
    # Set limit of 10 simultaneous RSS requests
    pool = Pool(10)

    # Get list of active Feed ids from database
    feed_query = Feed.select().where(Feed.inactive == 0)

    # Filter feed_query result list to feeds valid for current tick
    feed_query = [f for f in feed_query if (tick/f.refresh) == int(tick/f.refresh)]

    # loop over feeds found, spawn rss_worker(feed)

    for f in feed_query:
        pool.spawn(rss_worker, f)
    pool.join()

    # Disconnect from database
    db.close()

def rss_server_loop():

    c = Count() # initialise loop interval counter at 0

    logging.info("In rss_server_loop(), starting...")

    while True:
        # Get tick counter value
        tick = c.get()

        logging.info("Server loop: Interval tick %d", tick)

        # Call RSS server to spawn another query set
        # will pass current tick as parameter
        rss_spawn(tick)

        # wait INTERVAL seconds
        gevent.sleep(INTERVAL)

        # increment tick
        c.increment()

# --------------------------------------------------
# RSS Worker(update Feed f)
def rss_worker(f):
    """RSS gevent worker function"""
    logging.info("Starting reader process for feed %s", f.id)

    id = f.id

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
            Feed.update(errors=0).where(Feed.id == id)

        prefiltered=False

        # Get RSS/ATOM version number
        logging.info("Feed version: %s", d.version)

        # Catch status 301 Moved Permanently, update feed address
        if d.status == 301:
            Feed.update(url=d.href).where(Feed.id == id)

        # Conditional HTTP:
        # Check for Etag in result and write to DB
        if hasattr(d, 'etag'):
            logging.info("Etag: %s", d.etag)
            Feed.update(etag=d.etag).where(Feed.id == id)
            prefiltered=True

        # Conditional HTTP
        # Check for Last-Modified in result and write to DB
        if hasattr(d, 'modified'):
            logging.info("Modified %s", d.modified)
            Feed.update(last_modified=d.modified).where(Feed.id == id)
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
                p.feed = id
                p.save() # Save Post data to DB

            # Filter text for dangerous content (e.g. XSRF?)
            # Feedparser already does this to some extent

            # update Feed last checked date

            # Spawn websocket message with new posts for web client

    else: 
        # Site appears to be down
        logging.warning("Site %s is DOWN, status: %d", f.url, d.status)

        # Increment error counter
        Feed.update(errors = Feed.errors + 1).where(Feed.id == id)
        
        # Status 410 Gone Permanently, mark feed inactive
        if d.status == 410:
            Feed.update(inactive==True).where(Feed.id == id)

        # Spawn websocket message reporting error to web client

    return


# --------------------------------------------------
# Initialise: Startup message, DB creation check, load default feeds
def initialise():

    logging.info("Starting Wisewolf server version v0.04...")

    # Check for existence of SQLite3 database, creating if necessary
    if not os.path.exists(DB_FILE):
        create_db()

    # If feed table is empty, load the default feed set:
    
    if Feed.select().count() == 0:
        load_defaults()

    return

# --------------------------------------------------
# Start main RSS server loop
def start():

    gevent.joinall([gevent.spawn(rss_server_loop)])

# --------------------------------------------------
# interval counter class
# rolls over at 96

class Count:
    def __init__(self):
        self.counter = 0
    def get(self):
        return self.counter
    def increment(self):
        self.counter += 1
        if self.counter > 95:
            self.counter = 0

# --------------------------------------------------

if __name__ == '__main__':

    # Server startup options
    # --nows: no websocket output, just update DB

    parser = argparse.ArgumentParser(description="Wisewolf RSS server process")
    parser.add_argument("--nows", help="No websocket output, just update DB")
    args = parser.parse_args()

    # TODO: Handle 'headless' commandline options
    # TODO: Print startup messages

    # Log startup message, create DB if necessary
    initialise()

    # Start main RSS server loop
    start()
