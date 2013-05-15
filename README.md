Wisewolf
========

**Server-based RSS newsreader, with additional image-handling features. Replacement for Google Reader.**

The intent is to make Wisewolf an alternative to Tiny Tiny RSS: http://tt-rss.org/redmine/projects/tt-rss/wiki

Roadmap (intended for initial alpha)
---------

For v0.1 initial alpha:

* Feed aggregation
* OPML import

For v0.2

* Optionally strip embedded/linked images to associated galleries (see Yomiko). Useful for art sites and web comics

For v0.3

* mobile support (target Mobile Safari on iPad and iPhone). Swipe between articles, feeds.

Requirements
------------

* Python feedreader module
* A database. Will be SQlite3 in development, choice of MySQL or PostgreSQL in production
* ImageMagick _convert_ for thumbnail generation

Wisewolf runs on the _web2py_ Python web framework, and will require WSGI-compliant hosting.
