#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2015 Kyubi Systems: www.kyubi.co.uk
"""

# import system libraries
import feedparser
import argparse
import os
from dateutil.parser import *
from datetime import *
import pytz

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

# Define database
db = SqliteDatabase(DB_FILE, threadlocals=True)

# --------------------------------------------------
# RSS gevent parallel server process
# Default rss_spawn() will check all feeds in DB
def rss_spawn(tick=1):

    # Connect to database
    db.connect()
    
    # Set limit of MAX_REQUESTS simultaneous RSS requests
    pool = Pool(MAX_REQUESTS)

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
    error_count = f.errors

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
        logging.info("Feed %s is UP, status %s", f.url, str(d.status))

        # Reset error counter on successful connect
        if error_count > 0:
            q = Feed.update(errors=0).where(Feed.id == id)
            q.execute()

        # Get RSS/ATOM version number
        logging.info("Feed version: %s", d.version)

        # Catch status 301 Moved Permanently, update feed address
        if d.status == 301:
            q = Feed.update(url=d.href).where(Feed.id == id)
            q.execute()

        # Conditional HTTP:
        # Check for Etag in result and write to DB
        if hasattr(d, 'etag'):
            logging.info("Etag: %s", d.etag)
            q = Feed.update(etag=d.etag).where(Feed.id == id)
            q.execute()

        # Conditional HTTP
        # Check for Last-Modified in result and write to DB
        if hasattr(d, 'modified'):
            logging.info("Modified %s", d.modified)
            q = Feed.update(last_modified=d.modified).where(Feed.id == id)
            q.execute()

        # Check for feed modification date, write to DB
        if hasattr(d, 'published'):
            logging.info("Published: %s", d.published)

        if hasattr(d, 'updated'):
            logging.info("Updated: %s", d.updated)

        # Check for 'not-modified' status code, skip updates if found
        if d.status == 304:
            logging.info("Feed %s -- no updates found, skipping", f.url)
            return

        # If post entries exist, process them
        if d.entries:

            # Iterate over posts found
            # Build and add Post object to DB
            # DB write lock needed?
            for post in d.entries:
                
                # Get post date. Fall back to feed publication date :-(
                dt = post.get('published') or d.feed.published 
                dt = parse(dt) # convert to datetime

                # Correct post published datetime to UTC using pytz
                try:
                    published_date = dt.astimezone(pytz.utc) # TZ specified
                except ValueError: 
                    published_date = dt.replace(tzinfo=pytz.utc) # Naive, no TZ specified

                # Correct last-checked date to UTC using pytz
                lc = f.last_checked
                try:
                    last_checked = lc.astimezone(pytz.utc)
                except ValueError:
                    last_checked = lc.replace(tzinfo=pytz.utc)
                    
                if hasattr(d, 'modified'):
                    print 'modified', d.modified, type(d.modified)
                print 'published_date',published_date, type(published_date)
                print 'last_checked',f.last_checked, type(f.last_checked)

                # If published date newer than last feed check date, save new Post data to DB
                if published_date > last_checked:
                    p = Post()
                    p.title = post.get('title') or "No title"
                    p.description = post.get('description') or ""
                    p.published = published_date
                    p.content = post.get('content') or "No content"
                    p.link = post.get('link') or ""
                    p.feed = id
                    p.save()

            # TODO: Filter text for dangerous content (e.g. XSRF?)
            # Feedparser already does this to some extent

            # TODO: Spawn websocket message with new posts for web client

    else: 
        # Site appears to be down
        logging.warning("Feed %s is DOWN, status: %d", f.url, d.status)
        error_count += 1

        # Increment error counter
        # Mark feed inactive if MAX_ERRORS reached
        q = Feed.update(errors = error_count).where(Feed.id == id)
        q.execute()
        if error_count == MAX_ERRORS:
            q = Feed.update(inactive = True).where(Feed.id == id)
            q.execute()
        
        # Status 410 Gone Permanently, mark feed inactive
        if d.status == 410:
            q = Feed.update(inactive = True).where(Feed.id == id)
            q.execute()

        # TODO: Spawn websocket message reporting error to web client

    # update Feed last checked date before returning
    q = Feed.update(last_checked = datetime.now()).where(Feed.id == id)
    q.execute()
    return


# --------------------------------------------------
# Initialise: Startup message, DB creation check, load default feeds
def initialise():

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
    print "Wisewolf RSS server %s (c) Kyubi Systems 2015: initialising..." % SERVER_VERSION,
    initialise()
    print 'OK'

    # Start main RSS server loop
    logging.info("Wisewolf RSS server version %s starting" % SERVER_VERSION)
    start()
