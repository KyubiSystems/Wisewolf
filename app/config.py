"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

import os

# set application path
APP_PATH = os.path.dirname(os.path.realpath(__file__))

# Set DEBUG to True for development
DEBUG = True

# Set SQLite3 database file path
DB_FILE = APP_PATH + '/db/Wisewolf.db'

# Set path for downloaded image cache
CACHE_PATH = APP_PATH + '/cache/'
