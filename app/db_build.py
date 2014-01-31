#!/usr/bin/env python

from peewee import *
from models import *

# Define database
db = SqliteDatabase(DATABASE_URI)

# Connect to database
db.connect()

# Create tables
Category.create_table()
Feed.create_table()
Post.create_table()
