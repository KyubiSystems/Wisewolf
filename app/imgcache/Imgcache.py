#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2015 Kyubi Systems: www.kyubi.co.uk
"""
from models import *
from urlparse import urlparse
import urllib2

import logging
log = logging.getLogger('wisewolf.log')

import BeautifulSoup as BS

# Get favicon file for server and write to cache directory
# TODO: Delete favicon from cache when corresponding feed deleted from DB.

def getFavicon(id):

    feed = Feed.get(Feed.id == id)
    url = feed.url
    u = urlparse(url)
    favicon_url = 'http://' + u.netloc + '/favicon.ico'
    try:
        f = urllib2.urlopen(favicon_url)
    except urllib2.HTTPError:
        return None

    log.info("Favicon {0} status: {1}".format(str(id), str(f.getcode()))) 
    favicon_data = f.read()
    favicon_path = '{0}favicon_{1}.ico'.format(ICONS_PATH, str(id)) # Full filepath to favicon
    favicon_file = 'favicon_{1}.ico'.format(str(id)) # favicon filename

    with open(favicon_path, 'wb') as fav:
        fav.write(favicon_data)
    fav.close()

    # Return filename of favicon
    return favicon_file

# Get images from post HTML fragment and write to cache directory

def getImages(id):

    post = Post.get(Post.id == id)
    html = post.content

    soup = BS(html)
    for tag in soup.find_all('img'):
        image_url = tag['src']
        try:
            f = urllib2.urlopen(image_url)
            http = f.info()
            content_type = http.type  # Get HTTP Content-Type
        except urllib2.HTTPError:
            continue

        log.info("Found image {0}, writing to cache", image_url)

        image_data = f.read()

        # TODO: Construct image cache path and filename
        # Use HTTP content-type to decide extension
        # CACHE_PATH/[feed_id]/[post_id]_[image_number].[ext]
        # Create feed directory as required

        with open(image_path, 'wb') as img:
            img.write(image_data)
        img.close()
