"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

import os

# set version string
SERVER_VERSION = "v0.04"

# set application path
APP_PATH = os.path.dirname(os.path.abspath(__file__))

# Set DEBUG to True for development
DEBUG = True

# Set SQLite3 database file path
DB_FILE = APP_PATH + '/db/Wisewolf.db'

# Set default feeds for server
DEFAULTS_FILE = APP_PATH + '/DEFAULT_RSS'

# Set static path for Flask app
STATIC_PATH = APP_PATH + '/static/'

# Set path for downloaded image cache
CACHE_PATH = STATIC_PATH + 'cache/'

# Set path for downloaded images
IMAGE_PATH = CACHE_PATH + 'images/'

# Set path for thumbnails
THUMB_PATH = CACHE_PATH + 'thumbs/'

# Set default size for thumbnails
THUMB_SIZE = (150, 150)

# Set path for downloaded favicons
ICONS_PATH = CACHE_PATH + 'icons/'

# Maximum consecutive errors before feed marked inactive
MAX_ERRORS = 32

# Maximum simultaneous feed requests
MAX_REQUESTS = 10

# Set default reload interval to 15 minutes
INTERVAL = 900

# Set User-Agent string for Wisewolf reader
USER_AGENT = 'WisewolfRSS/0.0.4 +http://www.wisewolf.co.uk/'
