"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from flask import Flask, render_template, jsonify
from models import *
from messages import *

app = Flask(__name__)

# Index route -----------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # Load feeds from DB to display
    # List of categories
    # List of feeds by category
    # List of posts in order of publication date

    # Declare empty dict of feeds (emulate sparse list)
    feeds = {}

    # Get categories, number of posts by category
    categories = Category.select(Category, fn.Count(Post.id).alias('count')).join(Feed).join(Post).group_by(Category)

    # Loop over categories
    for c in categories:
        # Get feeds by category
        f = Feed.select().where(Feed.category == c.id).annotate(Post)
        feeds[c.id] = f

    # Get posts in decreasing date order
    posts = Post.select().order_by(Post.published.desc())

    # Render main page template
    return render_template("index.html", categories=categories, feeds=feeds, posts=posts)

# Post routes ----------------

@app.route('/post/<int:id>', methods=['GET'])
def get_post(id=None):
    # Get post #id from database
    try:
        post = Post.get(Post.id == id)
    except PostDoesNotExist:
        resp = jsonify(POST_NOT_FOUND)
        resp.status_code = 404
        return resp

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
    resp = jsonify(STATUS_OK)
    resp.status_code = 200
    return resp


# Feed routes ----------------

@app.route('/feed', methods=['GET'])
@app.route('/feed/<int:id>', methods=['GET'])
def feed(id=None):
    # Get feed number <id>
    try:
        feed = Feed.get(Feed.id == id)
    except FeedDoesNotExist:
        resp = jsonify(FEED_NOT_FOUND)
        resp.status_code = 404
        return resp

    # Get posts in decreasing date order
    posts = Post.select().where(Feed.id == id).order_by(Post.published.desc())

    # Select return format on requested content-type?
    # Return JSON here for client-side formatting?

    # Render feed page template
    return render_template("feed.html", feed=feed, posts=posts)

@app.route('/feed/', methods=['POST'])
@app.route('/feed/<int:id>', methods=['POST'])
def feed_update(id=None):

    # Manual update of one or all feeds now
    if request.json['action'] == 'refresh':
        
        # Call refresh routine
        # TODO: RSS worker functions in separate package
        # TODO: Need to capture return status
        if id == None:
            rss_spawn() # Update all feeds
        else:
            try:
                feed = Feed.get(Feed.id == id)
            except FeedDoesNotExist:
                resp = jsonify(FEED_NOT_FOUND)
                resp.status_code = 404
                return resp

            rss_worker(feed) # Update single feed
        
        # return JSON status OK
        resp = jsonify(STATUS_OK)
        resp.status_code = 200
        return resp

    # Mark one or all feeds read
    elif request.json['action'] == 'markread':

        if id == None:
            # Mark all posts read
            query = Post.update(is_read=True)
        else:
            # Mark posts in current feed read
            query = Post.update(is_read=True).where(Feed.id == id)
            
        query.execute()
            
    # return JSON status OK
        resp = jsonify(STATUS_OK)
        resp.status_code = 200
        return resp


# Manual add of feed url
@app.route('/feed/add', methods=['POST'])
def add_feed(url=None):
    
    # Get url and category submitted via AJAX
    url = request.json['url']
    category = request.json['category'] # From dropdown on submit form

    # url processing goes here
    # check content type for RSS?
    # Try autodetection and add to DB if found

    # If not found, return FEED_NOT_FOUND

    # return JSON status OK
    resp = jsonify(STATUS_OK)
    resp.status_code = 200
    return resp

@app.route('/feed/<int:id>', methods=['DELETE'])
def delete_feed(id=None):
    # Manual deletion of feed from database
    # TODO: Check and implement cascading delete
    # TODO: Some confirmation required?


    if id == None:

        # return feed not found
        resp = jsonify(FEED_NOT_FOUND)
        resp.status_code = 404
        return resp

    else:

        query = Post.delete().where(Feed.id == id)
        query.execute()

        query = Feed.delete().where(Feed.id == id)
        query.execute()

    # return JSON status OK
    resp = jsonify(STATUS_OK)
    resp.status_code = 200
    return resp


# Category routes ------------

@app.route('/category', methods=['GET'])
@app.route('/category/<int:id>', methods=['GET'])
def category(id=None):
    # Get category #id
    try:
        categories = Category.get(Category.id == id)
    except CategoryDoesNotExist:
        resp = jsonify(CATEGORY_NOT_FOUND)
        resp.status_code = 404
        return resp

    # Get feeds in category
    feeds = Feed.select().where(Category.id == id).annotate(Post)

    # Get posts in category in decreasing date order
    posts = Post.select().join(Feed).where(Category.id == id).order_by(Post.published.desc())

    # Return mode dependent on Content-Type?

    # Render category page template
    return render_template("category.html", categories=categories, feeds=feeds, posts=posts)

# Category delete
# Reassign all feeds in category to 'unsorted'?

@app.route('/category/<int:id>', methods=['DELETE'])
def delete_category(id):
    # Delete category #id
    query = Category.delete().where(Category.id == id)
    query.execute()

    # return JSON status OK
    resp = jsonify(STATUS_OK)
    resp.status_code = 200
    return resp

# Gallery routes -------------

@app.route('/gallery', methods=['GET'])
@app.route('/gallery/<int:id>', methods=['GET'])
def gallery(id=None):
    # Get gallery images associated with feed #id
    if id == None:
        images = Image.select()
    else:
        images = Image.select().where(Feed.id == id)

    return render_template("gallery.html", images=images)

# Image routes ---------------

@app.route('/image/<int:id>', methods=['GET'])
def get_image(id):
    # Get image #id
    try:
        image = Image.get(Image.id == id)
    except ImageDoesNotExist:
        resp = jsonify(IMAGE_NOT_FOUND)
        resp.status_code = 404
        return resp

    return render_template("image.html", image=image)

@app.route('/image/<int:id>', methods=['DELETE'])
def delete_image(id):
    # Get image #id
    try:
        image = Image.get(Image.id == id)
    except ImageDoesNotExist:
        resp = jsonify(IMAGE_NOT_FOUND)
        resp.status_code = 404
        return resp

    # TODO: Delete image binary file and thumb
    # Need to check safe path and MIME type first

    # Delete image DB record
    query = Image.delete().where(Image.id == id)
    query.execute()

    # return JSON status OK
    resp = jsonify(STATUS_OK)
    resp.status_code = 200
    return resp

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

# Websocket testing ----------

@app.route('/test/websocket')
def wstest():
    return render_template("ws_echo_client.html")

@app.route('/test/websocket2')
def wstest2():
    return render_template("ws_jsontime_client.html")

# Error handling -------------

@app.errorhandler(404)
def internal_error(error):
    return render_template("404.html", error=error), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html", error=error), 500
