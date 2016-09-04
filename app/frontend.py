#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2015 Kyubi Systems: www.kyubi.co.uk
"""

import os
import subprocess
import logging

from flask import Flask
from flask import g

app = Flask(__name__)

from config import *
from views import *
from db.DatabaseUtils import *

# Import configuration

if __name__ == '__main__':

    logger = logging.getLogger('werkzeug')
    handler = logging.FileHandler('access.log')
    logger.addHandler(handler)

    # Also add handler to Flask's logger
    #for cases when Werkzeug isn't underlying WSGI server
    app.logger.addHandler(handler)
    
    app.run(debug=True)
