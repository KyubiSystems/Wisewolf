"""
Wisewolf -- v.0.02

(c) 2013 -- KyubiSystems

Web-based RSS feed reader and image spider
Use SQLite3 database for initial development and testing
"""

import feedreader
import sqllite3

from flask import Flask
app = Flask(__name__)

# read config file

app.config.from_object('config')

print app.config['DATABASE_URI']

# CLASS DEFINITION ===================================================================

class Feed():
    """Feed() -- instantiate RSS feed object"""
    def __init__(self, address):
        self.id = 0
        self.address = address
        self.data = []
        self.count = 0
        self.description = 0

    def parse():
        self.data = feedparser.parse(self.address)

    def count():
        pass

class Article():
    """Article -- instantiate article object"""
    def __init__():
        self.id = 0
        self.text = ""
        self.date = ""

    def getText():
        pass

    def showText():
        pass

    def getImages():
        pass

    def deleteArticle():
        pass

class Tagset():
    """Tagset -- instantiate tag set object"""
    def __init__():
        self.id = 0
        self.name = []
        self.description = []

    def addTag():
        pass

    def deleteTag():
        pass

    def showTag():
        pass

# END CLASS DEFINITION ===============================================================
