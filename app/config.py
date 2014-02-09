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

# Set default feeds for server
DEFAULTS_FILE = APP_PATH + '/DEFAULT_RSS'

# Set path for downloaded image cache
CACHE_PATH = APP_PATH + '/cache/'

# Set path for downloaded favicons
ICONS_PATH = CACHE_PATH + 'icons/'

# Set User-Agent string for Wisewolf reader
USER_AGENT = 'WisewolfRSS/0.0.2a +http://www.wisewolf.co.uk/'
