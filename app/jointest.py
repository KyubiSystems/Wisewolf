from models import *

categories = Category.select(Category, fn.Count(Post.id).alias('count')).join(Feed).join(Post).group_by(Category)


for c in categories:
    print '----------'
    print c.name, ' - ', c.count, ' articles'

    feeds = Feed.select().where(Feed.category == c.id).annotate(Post)

    for f in feeds:
        print f.name, ' - ', f.count, ' articles'
