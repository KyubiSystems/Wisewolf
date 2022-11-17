Wisewolf API
============

Wisewolf uses a "REST-like" API for routine operations, returning JSON formatted responses.

|Route       | HTTP Query Type | Returns                      |
|------------|-----------------|------------------------------|
|/           | GET             | Top-level view               |
|/index      |                 |                              |
|            |                 |                              |
|/post/[id]  | GET             | Get post [id]                |
|            | DELETE          | Delete post [id]             |
|            |                 |                              |
|/feed       | GET             | Get posts from all feeds     |
|/feed/[id]  |                 | Get posts from feed [id]     |
|            |                 |                              |
|/feed       | POST            | **action='refresh'**: Get new posts |
|/feed/[id]  |                 |                              |
|            |                 |                              |  
|/feed       | POST            | **action='markread'**: Mark posts as read |
|/feed/[id]  |                 |                              |
|            |                 |                              |
|/feed/add   | POST            | Add new feed (accepts valid URL) |
|            |                 |                              |
|/feed/[id]  | DELETE          | Delete feed                  |
|            |                 |                              |
|/favourite/[id] | GET         | Get favourite status from post [id] |
|            | POST            | Toggle favourite status on post [id] |
|            |                 |                              |
|/category   | GET             | List categories              |
|/category/[id] |              | Get posts from category [id] |
|            |                 |                              |
|/category/[id] | DELETE       | Delete category [id], reassign feeds to 'Unsorted' |
|            |                 |                              |
|/gallery    | GET             | Show all scraped images      |
|/gallery/[id] |               | Show scraped images for feed [id] |  
|            |                 |                              |
|/image/[id] | GET             | Display image [id]           |
|            | DELETE          | Delete image [id]            |

**& more to follow...**

- settings update handler (POST)
- OPML import handler (POST)
