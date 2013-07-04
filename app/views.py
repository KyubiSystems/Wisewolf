from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

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
