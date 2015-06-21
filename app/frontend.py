#!/usr/bin/env python
"""
Wisewolf RSS Reader
(c) 2015 Kyubi Systems: www.kyubi.co.uk
"""

import os
import subprocess

from flask import Flask
from flask import g

from config import *
from views import *
from db.DatabaseUtils import *

# Import configuration

if __name__ == '__main__':

    app = Flask(__name__)
    
    app.run(debug=True)
