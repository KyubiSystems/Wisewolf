#!/usr/bin/env python

"""
Wisewolf -- v.0.01

(c) 2013 -- KyubiSystems

Web-based RSS feed reader and image spider
Use SQLite3 database for initial development and testing
"""

import feedreader
import sqllite3

from datetime import datetime
from file_utils import readConfig
from string import Template

# read config file

Config = readConfig('config.json')

# Print Content-Type: header + blank line
print "Content-type: text/html"
print

