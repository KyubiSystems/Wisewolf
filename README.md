Wisewolf
========

**Server-based RSS newsreader, with additional image-handling features. Replacement for Google Reader.**

The intent is to make Wisewolf an alternative to Tiny Tiny RSS: http://tt-rss.org/redmine/projects/tt-rss/wiki

**Current status: version 0.1-alpha**

API
---

Wisewolf has a ["REST-like" API for routine feed operations](https://github.com/KyubiSystems/Wisewolf/blob/master/docs/API.md).

Requirements
------------

* Use of a Python *virtualenv* environment is recommended.
* See Wisewolf-req.txt pip requirements file for Python prerequisites. 
* Relies on __Flask__ microframework and __Gevent/Greenlet__ for asynchronous communications. 
* A database. SQLite3 by default, look at supporting other DBMS (MySQL, Postgres).
* Pillow (Python Imaging Library fork) with libjpeg support for thumbnail generation.

Wisewolf requires WSGI-compliant hosting.

License
-------

Wisewolf uses the **Creative Commons BY-NC-SA 4.0 license**.

Roadmap for alpha release
---------

For v0.1-alpha:

- [x] Feed aggregation
- [x] Post display
- [x] OPML import
- [x] Asynchronous client updates
- [x] Refresh feeds automatically (update frequency selectable per feed) or manually.
- [x] Favourite posts

For v0.2

- [x] Strip web-bug images
- [x] Post formatting via Readability
- [ ] Live update of feed display via websockets
- [ ] Optionally strip embedded/linked images to associated local galleries (see Yomiko). Useful for art sites and webcomics
- [ ] Media support for HTML5 audio/video, MediaRSS ingest
- [ ] Hotkey support
- [ ] Mobile support. Swipe between articles, feeds.

For v0.3

- [ ] Text indexing, fulltext searching via Whoosh?
- [ ] Move from category to tag system?
- [ ] Docker packaging


For v1.0

- [ ] Multi-user support
- [ ] Optional social sharing for feed items (off by default)


Possible subsequent additions

* PubSubHubBub support


Screenshot
----------

A screenshot, because you asked. The front-end will change a great deal over coming versions.

<img src="https://github.com/KyubiSystems/Wisewolf/raw/master/screenshots/wisewolf-alpha0.04.3.jpg">