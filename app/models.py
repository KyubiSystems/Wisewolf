from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

# define category DB model class

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key = True)
    name = Column(String(256))
    comment = Column(String(256))
    feeds = relationship('Feed', backref='category', lazy='dynamic')

    def __init__(self, name, comment):
        self.name = name
        self.comment = comment

    def __repr__(self):
        return '<Category %r>' % self.name

# define feed DB model class

class Feed(Base):
    __tablename__ = 'feed'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(256))
    url = Column(String(512))
    category_id = Column(Integer, ForeignKey('category.id')) # Foreign Key field
    last_updated = Column(DateTime)
    comment = Column(String(256))
    strip_images = Column(Boolean)
    posts = relationship('Post', backref='feed', lazy='dynamic')

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

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key = True)
    title = Column(String(256))
    content = Column(Text)
    feed_id = Column(Integer, ForeignKey('feed.id')) # Foreign Key field
    post_date = Column(DateTime)
    is_read = Column(Boolean)
    is_favourite = Column(Boolean)

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


                           

