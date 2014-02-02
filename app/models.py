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
    url = CharField(max_length=512)
    category = ForeignKeyField(Category, related_name='feeds')
    last_updated = DateTimeField(default=datetime.datetime.now)
    comment = TextField()
    strip_images = BooleanField(default=False)
    refresh = IntegerField(default=1800)

class Post(BaseModel):
    title = CharField()
    link = CharField(max_length=512)
    content = TextField()
    feed = ForeignKeyField(Feed, related_name='posts')
    post_date = DateTimeField(default=datetime.datetime.now)
    is_read = BooleanField(default=False)
    is_favourite = BooleanField(default=False)
