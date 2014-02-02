#!/usr/bin/env python

from peewee import *
from models import *
import config

# Define database
db = SqliteDatabase(DB_FILE)

# Connect to database
db.connect()

# Create tables
Category.create_table()
Feed.create_table()
Post.create_table()
