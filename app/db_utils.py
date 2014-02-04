#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""
from models import *


# Create SQLite3 tables
def create_db():

    # Define database
    db = SqliteDatabase(DB_FILE)

    # Connect to database
    db.connect()

    # Create tables
    Category.create_table()
    Feed.create_table()
    Post.create_table()


# load default feeds in DB
def load_defaults():
    pass
