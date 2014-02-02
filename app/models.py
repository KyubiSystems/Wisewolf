#!/usr/bin/env python

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
    url = CharField()
    category_id = ForeignKeyField(Category, related_name='catname')
    last_updated = DateTimeField(default=datetime.datetime.now)
    comment = TextField()
    strip_images = ()

class Post(BaseModel):
    title = CharField()
    content = TextField()
    feed_id = ForeignKeyField(Feed, related_name='feedid')
    post_date = DateTimeField(default=datetime.datetime.now)
    is_read = BooleanField()
    is_favourite = BooleanField()
