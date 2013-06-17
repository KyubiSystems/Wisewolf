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

* Optionally strip embedded/linked images to associated local galleries (see Yomiko). Useful for art sites and webcomics

For v0.3

* Social sharing for feed items
* mobile support (target Mobile Safari on iPad and iPhone). Swipe between articles, feeds.

Requirements
------------

* See Wisewolf-req.txt pip requirements file for Python prerequisites. Relies on __Flask__ microframework and __Tornado__ for asynchronous communications.
* A database. Will be SQLite3 in development, choice of MySQL or PostgreSQL in production
* ImageMagick _convert_ for thumbnail generation for image galleries

Wisewolf requires WSGI-compliant hosting.

