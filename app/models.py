#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from config import *
from peewee import *
import datetime

# define database
db = SqliteDatabase(DB_FILE)

# create base model class that application models will extend


class BaseModel(Model):
    class Meta:
        database = db


class Category(BaseModel):
    name = CharField()
    comment = TextField()


class Feed(BaseModel):
    name = CharField()
    url = CharField(max_length=512)
    category = ForeignKeyField(Category, related_name='feeds')
    last_updated = DateTimeField(default=datetime.datetime.now())
    last_modified = CharField(max_length=64)
    etag = CharField(max_length=64)
    comment = TextField()
    strip_images = BooleanField(default=False)
    refresh = IntegerField(default=1800)
    expire = IntegerField(default=0)
    errors = IntegerField(default=0)


class Post(BaseModel):
    title = CharField()
    link = CharField(max_length=512)
    content = TextField()
    feed = ForeignKeyField(Feed, related_name='posts')
    post_date = DateTimeField(default=datetime.datetime.now())
    is_read = BooleanField(default=False)
    is_favourite = BooleanField(default=False)


class Image(BaseModel):
    feed = ForeignKeyField(Feed, related_name='images')
    post = ForeignKeyField(Post, related_name='images')
    path = CharField()
    thumb = CharField(max_length=512)
    date_created = DateTimeField(default=datetime.datetime.now())