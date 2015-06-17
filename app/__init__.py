"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

import os
import subprocess

from flask import Flask
from flask import g

# Import configuration

app = Flask(__name__)

# Get script directory

wd = os.path.dirname(os.path.realpath(__file__))

# Start RSS server backend

print "Wisewolf RSS server v0.04 starting... ",
subprocess.Popen(["./server.py"], cwd=wd)
print 'OK'

