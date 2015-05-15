Wisewolf API
============

Wisewolf uses a "REST-like" API for routine operations, returning JSON formatted responses.

Route	      | HTTP Query Type | Returns
--------------|-----------------|------------------------------
/	      |	GET		| Top-level view
/index        |                 |
	      |			|
/post/[id]    |	DELETE		| Delete post
	      |			|
/feed	      | GET		| Get posts from all feeds
/feed/[id]    |			| Get posts from feed [id]
	      |			|
/feed	      |	POST		| action='refresh': Get new posts
/feed/[id]    |			|
	      |			|
/feed	      |	POST		| action='markread': Mark posts as read
/feed/[id]    |			|
	      |			|
/feed/add     |	POST		| Add new feed
	      |			|
/feed/[id]    |	DELETE		| Delete feed
	      |			|
/category     |	GET		| List categories
/category/[id]|			| Get posts from category [id]
 	      |			|
/gallery      |	GET		| Show all scraped images
/gallery/[id] |			| Show scraped images for feed [id]		
	      |			|
/settings     |	GET		| Display program settings
	      |			|
/import	      | GET		| Form to import OPML


*& more to follow...*
- get post(!!)
- delete category
- get image
- delete image
- settings update handler (POST)
- OPML import handler (POST)
