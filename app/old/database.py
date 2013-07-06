from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

# initialise SQLAlchemy object

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./db/database.db"
db = SQLAlchemy(app)

# begin model definition

# define category DB model class

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256))
    comment = db.Column(db.String(256))
    feeds = db.relationship('Feed', backref='category', lazy='dynamic')

    def __init__(self, name, comment):
        self.name = name
        self.comment = comment

    def __repr__(self):
        return '<Category %r>' % self.name

# define feed DB model class

class Feed(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256))
    url = db.Column(db.String(512))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id')) # Foreign Key field
    last_updated = db.Column(db.DateTime)
    comment = db.Column(db.String(256))
    strip_images = db.Column(db.Boolean)
    posts = db.relationship('Post', backref='feed', lazy='dynamic')

    def __init__(self, name, url, category, comment, strip_images=False, last_updated=None):
        self.name = name
        self.url = url
        self.category = category
        self.comment = comment
        self.strip_images = strip_images
        if last_updated is None:
            last_updated = datetime.utcnow()
        self.last_updated = last_updated

    def __repr__(self):
        return '<Feed %r>' % self.name

# define post DB model class

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id')) # Foreign Key field
    post_date = db.Column(db.DateTime)
    is_read = db.Column(db.Boolean)
    is_favourite = db.Column(db.Boolean)

    def __init__(self, title, content, feed, post_date=None, is_read=False, is_favourite=False):
        self.title = title
        self.content = content
        if post_date is None:
            post_date = datetime.utcnow()
        self.post_date = post_date
        self.is_read = is_read
        self.is_favourite = is_favourite

    def __repr__(self):
        return '<Post %r>' % self.title


                           

