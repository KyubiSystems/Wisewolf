#!/bin/bash

# Start Wisewolf server backend

./app/server.py &

# Start Wisewolf web frontend

./frontend.py &
