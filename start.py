#!/usr/bin/env python

import os
import subprocess

# Get script directory

topdir = os.path.dirname(os.path.realpath(__file__))
appdir = topdir + '/app'

# Start Wisewolf RSS server backend

print "Wisewolf RSS server v0.04 starting... ",
subprocess.Popen(["./server.py"], cwd=appdir)
print 'OK'

# Start Wisewolf web frontend

print "Wisewolf frontend v0.04 starting... ",
subprocess.Popen(["./frontend.py"], cwd=appdir)
print 'OK'
