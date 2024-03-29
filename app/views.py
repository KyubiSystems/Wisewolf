"""
Wisewolf RSS Reader
(c) 2021 Kyubi Systems: www.kyubi.co.uk
"""

from flask import Flask, Response, redirect, url_for, send_from_directory, jsonify, \
    render_template, request
from models import Feed, Post, Category, Image, IntegrityError
from messages import CATEGORY_NOT_FOUND, DUPLICATE_FEED, FEED_NOT_FOUND, FEED_INVALID, \
    POST_NOT_FOUND, IMAGE_NOT_FOUND, STATUS_OK
from opml import Opml
from readability.readability import Document, Unparseable
from collections import defaultdict
import arrow
import autodiscovery
import requests
import os
import magic
import uuid
import urllib.request
import urllib.parse
import urllib.error
import json

from frontend import app

# Index route -----------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # Load feeds from DB to display
    # - List of categories
    # - List of feeds by category
    # - List of posts in order of publication date

    # Populate Category tree
    (categories, feeds) = loadTree()

    # Get posts in decreasing date order
    posts = Post.select().order_by(Post.published.desc()).paginate(1, 50)

    # Create human-readable datestamps for posts
    datestamps = loadDates(posts)

    # Render main page template
    return render_template("index.html",
                           categories=categories,
                           feeds=feeds,
                           posts=posts,
                           datestamps=datestamps)

# Post routes ----------------

@app.route('/post/<int:id>', methods=['GET'])
def get_post(id=None):
    # Get post #id from database
    try:
        post = Post.get(Post.id == id)
    except Post.DoesNotExist:
        return jsonify(**POST_NOT_FOUND)

    # Create human-readable datestamps for posts
    datestamp = loadDates([post,])

    # optional retrieve full article
    if not post.content:
        if post.link:
            rawhtml = urllib.request.urlopen(post.link).read()
            try:
                rawarticle = Document(rawhtml).summary()
            except Unparseable:
                rawarticle = 'Unable to parse article'
            post.content = rawarticle.strip()

#            print '>>>DEBUG: ' + post.content
    if request.json is None:

        # populate Category tree
        (categories, feeds) = loadTree()

        # render post HTML template
        return render_template("post.html",
                               categories=categories,
                               feeds=feeds,
                               p=post,
                               datestamp=datestamp)

    else:

        # Return post as JSON
        resp = jsonify(post)
        resp.status_code = 200
        return resp


@app.route('/post/<int:id>', methods=['DELETE'])
def delete_post(id=None):
    # Delete post #id from database
    query = Post.delete().where(Post.id == id)
    query.execute()

    # return JSON status OK
    return jsonify(**STATUS_OK)

@app.route('/favourite/<int:id>', methods=['GET'])
def get_favourite(id=None):
    # Get favourite status for post #id
    try:
        fav = Post.get(Post.id == id)
    except Post.DoesNotExist:
        return jsonify(**POST_NOT_FOUND)

    # return post fav status as JSON
    resp = jsonify(fav.is_favourite)
    resp.status_code = 200
    return resp

@app.route('/favourite/<int:id>', methods=['POST'])
def set_favourite(id=None):
    # Toggle favourite status for post #id
    try:
        is_favourite = Post.get(Post.id == id).is_favourite
        query = Post.update(is_favourite=not is_favourite).where(Post.id == id)
        query.execute()
    except Post.DoesNotExist:
        return jsonify(**POST_NOT_FOUND)

    # return JSON status OK
    return jsonify(**STATUS_OK)

# Feed routes ----------------

# Manage installed feeds
@app.route('/feed', methods=['GET'])
def managefeeds():

    # Get feeds from database along with post numbers
    feedlist = Feed.select().order_by('name').annotate(Post)

    datestamps = {}

    # Set reference timestamp to one week ago
    weekago = arrow.utcnow().replace(days=-7)

    for f in feedlist:
        updated = arrow.get(f.last_checked)

        # if feed newer than one week, print date in human format
        if updated > weekago:
            datestamps[f.id] = updated.humanize()
        else:
            datestamps[f.id] = updated.format('YYYY-MM-DD HH:mm')

    return render_template("managefeeds.html",
                           datestamps=datestamps,
                           feedlist=feedlist)


@app.route('/feed/<int:id>', methods=['GET'])
def feed(id=None):
    # Get feed number <id>
    try:
        feed = Feed.get(Feed.id == id)
    except Feed.DoesNotExist:
        return jsonify(**FEED_NOT_FOUND)

    # populate Category tree
    (categories, feeds) = loadTree()

    # Get posts in decreasing date order
    posts = Post.select().join(Feed).where(Feed.id == id).order_by(Post.published.desc()).paginate(1, 50)

    # Create human-readable datestamps for posts
    datestamps = loadDates(posts)

    # Select return format on requested content-type?
    if request.json is None:
        # Render feed page template
        return render_template("feed.html",
                               categories=categories,
                               feeds=feeds,
                               feed=feed,
                               posts=posts,
                               datestamps=datestamps)

    else:
        # Return JSON here for client-side formatting?
        return jsonify(response=[dict(feed=feed, posts=posts)])


@app.route('/feed/', methods=['POST'])
@app.route('/feed/<int:id>', methods=['POST'])
def feed_update(id=None):

    # Manual update of one or all feeds now
    if request.json['action'] == 'refresh':

        # Call refresh routine
        # TODO: RSS worker functions in separate package
        # TODO: Need to capture return status
        if id is None:
            rss_spawn() # Update all feeds
        else:
            try:
                feed = Feed.get(Feed.id == id)
            except Feed.DoesNotExist:
                return jsonify(**FEED_NOT_FOUND)

            rss_worker(feed) # Update single feed

        # return JSON status OK
        return jsonify(**STATUS_OK)

    # Mark one or all feeds read
    elif request.json['action'] == 'markread':

        if id is None:
            # Mark all posts read
            query = Post.update(is_read=True)
        else:
            # Mark posts in current feed read
            query = Post.update(is_read=True).where(Feed.id == id)

        query.execute()

    # return JSON status OK
        return jsonify(**STATUS_OK)


# Manual add of feed url
@app.route('/feed/add', methods=['POST'])
def add_feed(url=None):

    # Get url submitted via AJAX
    url = request.json['url']

    FEED_TYPES = ('application/rss+xml',
                  'text/xml',
                  'application/atom+xml',
                  'application/x.atom+xml',
                  'application/x-atom+xml')

    # Check if url already exists in feed DB
    dupe = Feed.select().where(Feed.url == url).count()
    if dupe > 0:
        return jsonify(**DUPLICATE_FEED)

    # Attempt to retrieve URL
    try:
        r = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        return jsonify(**FEED_NOT_FOUND)

    # check request status code
    if r.status_code != requests.codes.ok:
        return jsonify(**FEED_NOT_FOUND)

    # Get Content-Type
    contenttype = r.headers['content-type']

    # If Content-type is RSS, add it directly
    if contenttype in FEED_TYPES:
        feed = Feed.create(url=url)
        return jsonify(**STATUS_OK)

    # If Content-type is HTML, pass to autodiscovery
    if contenttype == 'text/html':

        p = autodiscovery.Discover()
        p.feed(r.text)

        # check result in case of no feeds found
        if len(p.feeds) == 0:
            return jsonify(**FEED_NOT_FOUND)
        else:
            # TODO: Could loop over all available feeds found?
            fulluri = p.feeds[0]['fulluri'] # just adds first feed found
            feed = Feed.create(url=fulluri)
            return jsonify(**STATUS_OK)

    # dropped through to here, feed must be invalid
    return jsonify(**FEED_INVALID)

@app.route('/feed/<int:id>', methods=['DELETE'])
def delete_feed(id=None):
    # Manual deletion of feed from database
    # TODO: Some confirmation required? Client JS via modal?
    if id is None:

        # return feed not found
        return jsonify(**FEED_NOT_FOUND)

    else:

        # TODO: Test ON DELETE CASCADE to Post table (should work)
        query = Feed.delete().where(Feed.id == id)
        query.execute()

    # return JSON status OK
    return jsonify(**STATUS_OK)


# Category routes ------------

@app.route('/category', methods=['GET'])
@app.route('/category/<int:id>', methods=['GET'])
def category(id=None):
    # Get category #id
    try:
        category = Category.get(Category.id == id)
    except Category.DoesNotExist:
        return jsonify(**CATEGORY_NOT_FOUND)

    # Populate Category tree
    (categories, feeds) = loadTree()

    # Get posts in category in decreasing date order
    posts = Post.select().join(Feed).join(Category).where(Category.id == id).order_by(Post.published.desc()).paginate(1, 50)

    # Create human-readable datestamps for posts
    datestamps = loadDates(posts)

    # Return mode dependent on Content-Type?
    if request.json is None:

        # Render category page template
        return render_template("category.html",
                               category=category,
                               categories=categories,
                               feeds=feeds,
                               posts=posts,
                               datestamps=datestamps)

    else:

        # Return JSON data structure
        return jsonify(response=[dict(categories=categories, feeds=feeds, posts=posts)])

# Category delete
@app.route('/category/<int:id>', methods=['DELETE'])
def delete_category(id):
    # Delete category #id
    # Reassign all feeds in category to 'unsorted' id 0?
    query = Feed.update(category_id=0).where(Category.id == id)
    query.execute()

    query = Category.delete().where(Category.id == id)
    query.execute()

    # return JSON status OK
    return jsonify(**STATUS_OK)

# Gallery routes -------------

@app.route('/gallery', methods=['GET'])
@app.route('/gallery/<int:id>', methods=['GET'])
def gallery(id=None):
    # Get gallery images associated with feed #id
    if id is None:
        images = Image.select()
    else:
        images = Image.select().where(Feed.id == id).paginate(1, 50)

    return render_template("gallery.html",
                           images=images)

# Image routes ---------------

@app.route('/image/<int:id>', methods=['GET'])
def get_image(id):
    # Get image #id
    try:
        image = Image.get(Image.id == id)
    except Image.DoesNotExist:
        return jsonify(**IMAGE_NOT_FOUND)

    return render_template("image.html", image=image)

@app.route('/image/<int:id>', methods=['DELETE'])
def delete_image(id):
    # Get image #id
    try:
        image = Image.get(Image.id == id)
    except Image.DoesNotExist:
        return jsonify(**IMAGE_NOT_FOUND)

    # TODO: Delete image binary file and thumb
    # Need to check safe path and MIME type first

    # Delete image DB record
    query = Image.delete().where(Image.id == id)
    query.execute()

    # return JSON status OK
    return jsonify(**STATUS_OK)

# Management routes ----------

@app.route('/settings', methods=['GET'])
def settings():
    # Gather settings values and pass to view...

    return render_template("settings.html")

# route for processing settings update...

# Import OPML
@app.route('/import', methods=['GET'])
def opml_import():
    return render_template("import.html")

# route for processing OPML import...
@app.route('/import/parse', methods=['POST'])
def opml_parse():

    UPLOAD_FOLDER = os.path.realpath('.') + '/static/uploads'
    file = request.files['file']
    if file and allowed_file(file.filename):
        opml_filename = str(uuid.uuid4()) + '.xml' # use UUID as unique uploaded filename root
        opml_path = os.path.join(UPLOAD_FOLDER, opml_filename)

        file.save(opml_path)

        print('OPML uploaded OK!')

        # run Opml parser on uploaded file
        o = Opml.OpmlReader(opml_path)
        o.parseOpml()

        print('OPML parsed OK!')

        # Save categories to DB, skip invalid or duplicate feeds
        for c in o.categories:
            try:
                cat = Category.create(name=c)
                cat.save()

            except IntegrityError:
                pass

        print('Categories added to DB!')

        # Iterate over feeds found
        for f in o.feeds:

            print('------------')
            print(f)

            # Get corresponding Category id
            cat_id = Category.get(Category.name == f['category']).id

            if o.version == "1.0":
                # Add feed from OPML version 1.0
                # TODO: Exception handling
                feed = Feed.create(name=f['text'], category=cat_id, version=f['type'], url=f['url'])
            elif o.version == "1.1" or o.version == "2.0":
                # Add feed from OPML version 1.1
                # TODO: Exception handling
                feed = Feed.create(name=f['title'], category=cat_id, version=f['type'],
                                   comment=f['text'], description=f['description'], url=f['xmlUrl'])
            else:
                continue

            # Add feed to DB, skip invalid or duplicate feeds
            try:
                feed.save()
            except IntegrityError:
                pass

        print('Feeds added to DB!')

        # return send_from_directory(UPLOAD_FOLDER, opml_filename)
        # Test returning uploaded OPML file
        return redirect(url_for('index'), code=302)

    return "<h1>Oops, something went wrong here...</h1>file extension is " +  os.path.splitext(file.filename)[1]

# Check for allowed file extensions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['.xml', '.opml'])
    return '.' in filename and os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS

# Websocket testing ----------

@app.route('/test/websocket')
def wstest():
    return render_template("ws_echo_client.html")

@app.route('/test/websocket2')
def wstest2():
    return render_template("ws_jsontime_client.html")

# JSON tree testing ----------

@app.route('/test/jsontree')
def jsontree():
    return loadJsonTree()

@app.route('/test/jsonmenu')
def jsontest():
    return render_template("jsonmenu.html")

# Error handling -------------

@app.errorhandler(404)
def internal_error(error):
    return render_template("404.html", error=error), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html", error=error), 500

# Populate Category tree -------------------------------

def loadTree():

    # Declare empty dict of feeds (emulate sparse list)
    feeds = {}

    # Get categories, number of posts by category
    categories = Category.select(Category, fn.Count(Post.id).alias('count')).join(Feed).join(Post).group_by(Category)

    # Loop over categories
    for c in categories:
        # Get feeds by category
        f = Feed.select().where(Feed.category == c.id).annotate(Post)
        feeds[c.id] = f

    return (categories, feeds)

def loadJsonTree():

    # Use collection to build nested list for tree
    feeds = defaultdict(list)

    # Get categories, number of posts by category
    categories = Category.select(Category, fn.Count(Post.id).alias('count')).join(Feed).join(Post).group_by(Category)

    # Loop over categories
    all_feeds = []
    for c in categories:

        feeds[c.id] = {'name': c.name, 'id' : c.id, 'count': c.count, 'children' : []}
        # Get feeds by category
        category_feeds = Feed.select().where(Feed.category == c.id).annotate(Post)
        for f in category_feeds:
            feeds[c.id]['children'].append({'id': f.id, 'name': f.name, 'count' : f.count, 'url': f.url})

        all_feeds.append(feeds[c.id])

    return Response(json.dumps(all_feeds), mimetype='application/json')


# Create human-readable datestamps for posts ------------

def loadDates(posts):

    datestamps = {}

    # Set reference timestamp to one week ago
    weekago = arrow.utcnow().replace(days=-7)

    # Loop over posts
    for p in posts:
        published_date = arrow.get(p.published)

        # if post newer than one week, print date in human format
        if published_date > weekago:
            datestamps[p.id] = published_date.humanize()
        else:
            datestamps[p.id] = published_date.format('YYYY-MM-DD HH:mm')

    return datestamps
