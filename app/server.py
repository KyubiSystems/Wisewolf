#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2015 Kyubi Systems: www.kyubi.co.uk
"""

# import system libraries
import feedparser
import argparse
import os
import arrow
import hashlib
import re
import HTMLParser

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
    if 'etag' in f:
        d = feedparser.parse(f.url, etag=f.etag)
    elif 'last_modified' in f:
        d = feedparser.parse(f.url, modified=f.last_modified)
    else:
        d = feedparser.parse(f.url)

    # Check returned HTTP status code
    if 'status' in d and d.status < 400:
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
        if 'etag' in d:
            logging.info("Etag: %s", d.etag)
            q = Feed.update(etag=d.etag).where(Feed.id == id)
            q.execute()

        # Conditional HTTP
        # Check for Last-Modified in result and write to DB
        if 'modified' in d:
            logging.info("Modified %s", d.modified)
            q = Feed.update(last_modified=d.modified).where(Feed.id == id)
            q.execute()

        # Check for feed modification date, write to DB
        if 'published' in d:
            logging.info("Published: %s", d.published)

        if 'updated' in d:
            logging.info("Updated: %s", d.updated)

        # Check for 'not-modified' status code, skip updates if found
        if d.status == 304:
            logging.info("Feed %s -- no updates found, skipping", f.url)
            return

        # If post entries exist, process them
        for post in d.entries:
            
            post_content = ""
            post_title = post.get('title', 'No title')

            h = HTMLParser.HTMLParser()
            desc = post.get('description', '')
            desc = h.unescape(desc) # unescape HTML entities
            post_description = re.sub(r'<[^>]*?>', '', desc) # crudely strip HTML tags in description
            
            post_published = arrow.get(post.get('published_parsed')) or arrow.now()
            if 'content' in post:
                post_content = post.content[0].value
            post_link = post.get('link', '')
                
            # Get post checksum (title + description + link url)
            check_string = (post_title + post_description + post_link).encode('utf8')
            post_checksum = hashlib.sha224(check_string).hexdigest()
            
            # If post checksum not found in DB, add post
            if Post.select().where(Post.md5 == post_checksum).count() == 0:
                p = Post()
                p.title = post_title
                p.description = post_description
                p.published = post_published.datetime  # convert from Arrow to datetime for DB
                p.content = post_content
                p.link = post_link
                p.feed = id
                p.md5 = post_checksum
                p.save()
                
            # TODO: Filter text for dangerous content (e.g. XSRF?)
            # Feedparser already does this to some extent

            # TODO: Spawn websocket message with new posts for web client

    else: 
        # Site appears to be down

        # Increment error counter
        # Mark feed inactive if MAX_ERRORS reached
        error_count += 1
        q = Feed.update(errors = error_count).where(Feed.id == id)
        q.execute()
        if error_count == MAX_ERRORS:
            q = Feed.update(inactive = True).where(Feed.id == id)
            q.execute()
            logging.warning("Feed %s is marked INACTIVE, MAX_ERRORS reached", f.url)
        
        # No valid status, skip feed now
        if not 'status' in d:
            logging.warning("Feed %s is DOWN, no valid status", f.url)
            return

        # Status 410 Gone Permanently, mark feed inactive
        if d.status == 410:
            q = Feed.update(inactive = True).where(Feed.id == id)
            q.execute()
            logging.warning("Feed %s is marked INACTIVE, 410 Gone Permanently", f.url)

        logging.warning("Feed %s is DOWN, status: %d", f.url, d.status)

        # TODO: Spawn websocket message reporting error to web client

    # update Feed last checked date before returning
    a = arrow.utcnow()
    q = Feed.update(last_checked = a.datetime).where(Feed.id == id)
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
