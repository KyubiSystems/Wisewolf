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

@app.route('/post/<int:id>', methods=['DELETE'])
def delete_post(id=None):
    # Delete post #id from database
    if id == None:

        resp = jsonify(POST_NOT_FOUND)
        resp.status_code = 404
        return resp

    else:
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
    feed = Feed.get(Feed.id == id)

    # Get posts in decreasing date order
    posts = Post.select().where(Post.id == id).order_by(Post.published.desc())

    # Select return on requested content-type?
    # Return JSON here for client-side formatting?

    # Render feed page template
    return render_template("feed.html", feed=feed, posts=posts)

@app.route('/feed/', methods=['POST'])
@app.route('/feed/<int:id>', methods=['POST'])
def feed_update(id=None):

    # Manual update of one or all feeds now
    if request.json['action'] == 'refresh':
        
        # Call refresh routine (see server.py)
        # TODO: RSS package?
        
        
        # return JSON status OK
        resp = jsonify(STATUS_OK)
        resp.status_code = 200
        return resp

    # Mark one or all feeds read
    elif request.json['action'] == 'markread':

        if id == None:
            query = Post.update(is_read=True)
        else:
            query = Post.update(is_read=True).where(Post.feed_id == id)
            
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
    category = request.json['category']

    # url processing goes here
    # check content type for RSS
    # if plain HTML try autodetection


    # return JSON status OK
    resp = jsonify(STATUS_OK)
    resp.status_code = 200
    return resp

@app.route('/feed/<int:id>', methods=['DELETE'])
def delete_feed(id=None):
    # Manual deletion of feed from database
    # TODO: Check and implement cascading delete

    if id == None:

        # return feed not found
        resp = jsonify(FEED_NOT_FOUND)
        resp.status_code = 404
        return resp

    else:

        query = Post.delete().where(Post.feed_id == id)
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
    # Get category number <id>
    categories = Category.get(Category.id == id)

    # Get feeds in category
    feeds = Feed.select().where(Feed.category == id).annotate(Post)

    # Get posts in category in decreasing date order
    posts = Post.select().join(Feed).where(Feed.category == id).order_by(Post.published.desc())

    # Render category page template
    return render_template("category.html", categories=categories, feeds=feeds, posts=posts)

# Gallery routes -------------

@app.route('/gallery', methods=['GET'])
@app.route('/gallery/<int:id>', methods=['GET'])
def gallery(id=None):
    # Get gallery images associated with feed #id
    if id == None:
        images = Image.select()
    else:
        images = Image.select().where(Image.feed_id == id)

    return render_template("gallery.html", images=images)

# Management routes ----------

@app.route('/settings')
def settings():
    return render_template("settings.html", methods=['GET'])

# Import OPML
@app.route('/import')
def opml_import():
    return render_template("import.html", methods=['GET'])

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
