#!/bin/sh

# Get version number
. ./VERSION

# Build lightweight alpine distro
docker build -t kyubi/wisewolf:latest -t kyubi/wisewolf:v$VERSION -f Dockerfile.alpine .
