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
    n = count_category_unread(3)
    return render_template("index.html", number=n)

@app.route('/feed')
def feed():
    return render_template("feed.html")

@app.route('/manage')
def manage():
    return render_template("manage.html")

@app.route('/category')
def category():
    return render_template("category.html")

@app.route('/settings')
def settings():
    return render_template("settings.html")

@app.route('/import')
def opml_import():
    return render_template("import.html")

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

@app.route('/hello')
def hello_world():
    return 'Hello world!'

# Error handling

@app.errorhandler(404)
def internal_error(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500
