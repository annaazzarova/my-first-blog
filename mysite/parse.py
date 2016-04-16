from django.utils import timezone
import feedparser
import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
application = get_wsgi_application()

from blog.models import Post

def grabPosts(request):
    d = feedparser.parse('http://tnt-dance.ru/load/rss/')
    for e in d.entries:
        post = Post()
        post.title = e.title
        post.text = e.summary
        post.url = e.link
        post.published_date = timezone.now()
        post.author = request.user
        post.save()

        print ("Title: " + e.title)
        print ("Link: " + e.link)
        print ("Content: " + e.summary)