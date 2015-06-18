"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

import os
import subprocess

from flask import Flask
from flask import g

from config import *
from views import *
from db.DatabaseUtils import *

# Import configuration

app = Flask(__name__)


