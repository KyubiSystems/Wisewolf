"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from flask import Flask, render_template
from models import *

app = Flask(__name__)

@app.route('/')
@app.route('/index')
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

# Feed routes ----------------

@app.route('/feed')
@app.route('/feed/<int:id>')
def feed(id=None):
    # Get feed number <id>
    feed = Feed.get(Feed.id == id)

    # Get posts in decreasing date order
    posts = Post.select().where(Post.id == id).order_by(Post.published.desc())

    # Render feed page template
    return render_template("feed.html", feed=feed, posts=posts)

@app.route('/feed/all/refresh')
@app.route('/feed/<int:id>/refresh')
def refresh(id=None):
    # Manual update of one or all feeds
    
    return True

@app.route('/feed/all/markread')
@app.route('/feed/<int:id>/markread')
def markread(id=None):
    # Manual markread of one or all feeds

    return True

@app.route('/feed/<int:id>/delete')
def delete(id=None):
    # Manual deletion of feed from database

    return True

# Category routes ------------

@app.route('/category')
@app.route('/category/<int:id>')
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

@app.route('/gallery')
@app.route('/gallery/<int:id>')
def gallery(id=None):
    # Get gallery images associated with feed #id
    return render_template("gallery.html")

# Management routes ----------

@app.route('/settings')
def settings():
    return render_template("settings.html")

# Import OPML
@app.route('/import')
def opml_import():
    return render_template("import.html")

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
