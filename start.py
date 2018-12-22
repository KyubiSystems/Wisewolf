#!/usr/bin/env python

import os
import subprocess

# Get script directory

topdir = os.path.dirname(os.path.realpath(__file__))
appdir = topdir + '/app'

# Start Wisewolf RSS server backend

print("Wisewolf RSS server starting... ", end=' ')
subprocess.Popen(["./server.py"], cwd=appdir)
print('OK')

# Start Wisewolf web frontend

print("Wisewolf frontend starting... ", end=' ')
subprocess.Popen(["./frontend.py"], cwd=appdir)
print('OK')
