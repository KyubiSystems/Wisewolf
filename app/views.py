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

    # Declare empty array of feeds
    feeds = []

    # Get categories, number of posts by category
    categories = Category.select(Category, fn.Count(Post.id).alias('count')).join(Feed).join(Post).group_by(Category)

    # Loop over categories
    for c in categories:
        # Get feeds by category
        f = Feed.select().where(Feed.category == c.id).annotate(Post)
        feeds.append(f)

    # Get posts in decreasing date order
    posts = Post.select().order_by(Post.published.desc())

    # Render main page template
    return render_template("index.html", categories=categories, feeds=feeds, posts=posts)

@app.route('/feed')
@app.route('/feed/<id>')
def feed(id=None):
    # Get feed number <id>
    feed = Feed.select().where(Feed.id == id)

    # Get posts in decreasing date order
    posts = Post.select().where(Post.id == id).order_by(Post.published.desc())

    # Render feed page template
    return render_template("feed.html", feed=feed, posts=posts)

@app.route('/category')
@app.route('/category/<id>')
def category(id=None):
    # Get category number <id>
    categories = Category.select().where(Category.id == id)

    # Get feeds in category
    feeds = Feed.select().where(Feed.category == id).annotate(Post)

    # Get posts in category in decreasing date order
    posts = Post.select().join(Feed).where(Feed.category == id).order_by(Post.published.desc())

    # Render category page template
    return render_template("category.html", categories=categories, feeds=feeds, posts=posts)

@app.route('/manage')
def manage():
    return render_template("manage.html")

@app.route('/settings')
def settings():
    return render_template("settings.html")

@app.route('/import')
def opml_import():
    return render_template("import.html")

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

# Error handling

@app.errorhandler(404)
def internal_error(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500
