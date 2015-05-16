Wisewolf
========

**Server-based RSS newsreader, with additional image-handling features. Replacement for Google Reader.**

The intent is to make Wisewolf an alternative to Tiny Tiny RSS: http://tt-rss.org/redmine/projects/tt-rss/wiki


API
---

Wisewolf has a ["REST-like" API for routine feed operations](https://github.com/KyubiSystems/Wisewolf/blob/master/docs/API.md).

Requirements
------------

* See Wisewolf-req.txt pip requirements file for Python prerequisites. Relies on __Flask__ microframework and __Gevent/Greenlet__ for asynchronous communications. Use of a *virtualenv* environment is suggested.
* A database. Will be SQLite3 by default, look at supporting other DBMS (MySQL, Postgres).
* Pillow (Python Imaging Library fork) with libjpeg support for thumbnail generation.

Wisewolf requires WSGI-compliant hosting.

License
-------

Wisewolf uses the **Creative Commons BY-NC-SA 3.0 license*.

Roadmap (intended for initial alpha)
---------

For v0.1 initial alpha:

* Feed aggregation
* OPML import
* Asynchronous client updates
* Refresh feeds automatically (update frequency selectable per feed) or manually.

For v0.2

* Optionally strip embedded/linked images to associated local galleries (see Yomiko). Useful for art sites and webcomics
* Hotkey support

For v0.3

* Move from category to tag system?  
* Favourite posts
* Social sharing for feed items
* mobile support (target Mobile Safari on iPad and iPhone). Swipe between articles, feeds.

Possible subsequent additions

* PubSubHubBub support
* Text indexing, fulltext searching

