'''
RSS feeds for blog posts

@copyright: Copyright 2012 Faraz Masood Khan, mk.faraz@gmail.com
@author: Faraz Masood Khan
'''

from foo.blog.models import Post
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.syndication.views import Feed

site = Site.objects.get_current()

class RssFeedGenerator(Rss201rev2Feed):
    mime_type = u'application/rss+xml'        
    def add_root_elements(self, handler):        
        super(RssFeedGenerator, self).add_root_elements(handler)
        handler.startElement(u'image', {})
        handler.addQuickElement(u"url", u'http://%s%s%s' % (site.domain, settings.STATIC_URL, 'blog/img/logo-50x50.png'))
        handler.addQuickElement(u"title", unicode(site.name))
        handler.addQuickElement(u"link", u'http://%s' % site.domain)
        handler.endElement(u'image')
    
class LatestFeed(Feed):
    feed_type = RssFeedGenerator
   
    def title(self):
        return unicode(site.name)

    def link(self):
        return '';

    def description(self):
        return settings.META_DESCRIPTION

    def items(self):
        return Post.latest().order_by('-published')[:30]
    
    def item_title(self, feed):
        return unicode(feed.title)
    
    def item_description(self, feed):
        return feed.content
    
    def item_link(self, feed):
        return feed.get_absolute_url()
    
    def item_guid(self, feed):
        return self.item_link(feed)
    
    def item_author_name(self, feed):
        return unicode(feed.author)
         
    def item_pubdate(self, feed):
        return feed.published
    
    def item_categories(self, feed):
        return '' #feed.categories.split(',')