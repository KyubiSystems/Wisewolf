#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from config import *
from peewee import *
import datetime

# define database
db = SqliteDatabase(DB_FILE, threadlocals=True)

# create base model class that application models will extend


class BaseModel(Model):
    class Meta:
        database = db


class Category(BaseModel):
    name = CharField(unique=True)
    comment = TextField()


class Feed(BaseModel):
    name = CharField()
    url = CharField(max_length=512)
    category = ForeignKeyField(Category, related_name='feeds')
    version = CharField(max_length=10)
    last_updated = DateTimeField(default=datetime.datetime.now())
    last_modified = CharField(max_length=64, default='')
    etag = CharField(max_length=64, default='')
    comment = TextField()
    strip_images = BooleanField(default=False)
    refresh = IntegerField(default=1) # Frequency of feed refresh, in units of INTERVAL
    expire = IntegerField(default=0)  # Time to expire posts, 0 = never
    errors = IntegerField(default=0)  # Number of errors seen in feed loading
    inactive = BooleanField(default=False)
    favicon = CharField(max_length=64)


class Post(BaseModel):
    title = CharField()
    link = CharField(max_length=512)
    description = TextField()
    content = TextField()
    feed = ForeignKeyField(Feed, on_delete='cascade', related_name='posts')
    published = DateTimeField(default=datetime.datetime.now())
    is_read = BooleanField(default=False)
    is_favourite = BooleanField(default=False)


class Image(BaseModel):
    feed = ForeignKeyField(Feed, related_name='images')
    post = ForeignKeyField(Post, related_name='images')
    path = CharField()
    thumb = CharField(max_length=512)
    date_created = DateTimeField(default=datetime.datetime.now())
