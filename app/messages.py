"""
Wisewolf RSS Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

POST_NOT_FOUND = {
    'status_code' : 404,
    'status' : 'Post not found'
    }

FEED_NOT_FOUND = {
    'status_code' : 404,
    'status' : 'Feed not found'
    }

CATEGORY_NOT_FOUND = {
    'status_code' : 404,
    'status' : 'Category not found'
    }

IMAGE_NOT_FOUND = {
    'status_code' : 404,
    'status' : 'Image not found'
    }

URL_NOT_FOUND = {
    'status_code' : 404,
    'status' : 'URL not found'
    }

FEED_INVALID = {
    'status_code' : 503,
    'status' : 'Not a valid RSS feed'
    }

DUPLICATE_FEED = {
    'status_code' : 503,
    'status' : 'Feed already exists in database'
}

STATUS_OK = {
    'status_code' : 200,
    'status' : 'OK'
    }
