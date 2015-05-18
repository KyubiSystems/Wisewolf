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

from bs4 import BeautifulSoup as BS
import os

from PIL import Image as Im

# Get favicon file for server and write to cache directory
# TODO: Delete favicon from cache when corresponding feed deleted from DB.


def getFavicon(feed_id):

    feed = Feed.get(Feed.id == feed_id)
    url = feed.url
    u = urlparse(url)
    favicon_url = 'http://' + u.netloc + '/favicon.ico'
    try:
        f = urllib2.urlopen(favicon_url)
    except urllib2.HTTPError:
        return None

    log.info("Favicon {0} status: {1}".format(str(id), str(f.getcode()))) 
    favicon_data = f.read()
    favicon_path = '{0}favicon_{1}.ico'.format(ICONS_PATH, str(id))  # Full file path to favicon
    favicon_file = 'favicon_{1}.ico'.format(str(id)) # favicon filename

    with open(favicon_path, 'wb') as fav:
        fav.write(favicon_data)
    fav.close()

    # Return filename of favicon
    return favicon_file

# Get images from post HTML fragment and write to cache directory


def getImages(post_id, makeThumb=True):

    # Image HTTP content types
    extensions = {'image/gif': 'gif', 'image/jpeg': 'jpg', 'image/pjpeg': 'jpg', 'image/png': 'png'}

    post = Post.get(Post.id == post_id)
    html = post.content
    feed = post.feed_id

    soup = BS(html)

    img_num = 0

    # Attempt to get images in HTML fragment
    for tag in soup.find_all('img'):
        image_url = tag['src']
        try:
            f = urllib2.urlopen(image_url)
            http = f.info()
            content_type = http.type  # Get HTTP Content-Type to determine file extension
        except urllib2.HTTPError:
            continue

        # If unrecognised content-type, skip this URL
        if content_type not in extensions:
            continue

        # TODO: Check image size, skip below size limit (avoids saving 1x1 pixel bugs)
        # Reasonable default would be existing thumbnail size

        # Check to see if URL already exists in Image table
        url_num = Image.select().where(Image.url == image_url).count()

        # If not found, add to cache
        if url_num == 0:

            log.info("Found image {0}, writing to cache", image_url)

            # Read image data from url
            image_data = f.read()

            # Create feed directory as required
            image_path = '{0}{1}'.format(IMAGE_PATH, str(feed))
            if not os.path.exists(image_path):
                os.makedirs(image_path)

            # Use HTTP content-type to decide extension
            # IMAGE_PATH/[feed_id]/[post_id]_[image_number].[ext]

            image_file = '{0}{1}/img_{2}.{3}'.format(IMAGE_PATH, str(feed), str(img_num), extensions[content_type])

            with open(image_file, 'wb') as img:
                img.write(image_data)
            img.close()

            # Add to Image database table
            Image.create(post_id=post_id, feed_id=feed, url=image_url, path=image_file)

            if makeThumb == True:

                # Create corresponding thumbnail using Pillow, add to thumbnail cache dir
                thumb_file = '{0}{1}/thumb_{2}.{3}'.format(THUMB_PATH, str(feed), str(img_num), extensions[content_type])

                try:
                    thumb = Im.open(image_file)
                    thumb.thumbnail(THUMB_SIZE)
                    thumb.save(thumb_file, "JPEG")
                except IOError:
                    log.error("Cannot create thumbnail for", image_file)

            # increment image counter
            img_num += 1

