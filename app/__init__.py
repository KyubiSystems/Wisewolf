"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from flask import Flask
from flask import g

# Import configuration

app = Flask(__name__)

# Import views
import server

# Initialise: Startup message, DB creation check, load default feeds
server.initialise()

# Start main RSS server loop
server.start()
