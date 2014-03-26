'''
Url for blog posts and categories

@copyright: Copyright 2012 Faraz Masood Khan, mk.faraz@gmail.com
@author: Faraz Masood Khan
'''

from django.conf.urls import url, patterns

from foo import settings 

urlpatterns = patterns('foo.blog.views',
                       url(r'^$', 'index', { 'page_index':0 }, name='foo_blog_index'),
                       url(r'^(?P<page_index>\d+)/$', 'index', name='foo_blog_index'),                       
                       url(r'^tag/(?P<tag>.+)/$', 'tag', { 'page_index':0 }, name='foo_blog_tag'),
                       url(r'^tag/(?P<tag>.+)/(?P<page_index>\d+)/$', 'tag', name='foo_blog_tag'),
                       url(r'^author/(?P<userid>\d+)/$', 'author', { 'page_index':0 }, name='foo_blog_author'),
                       url(r'^author/(?P<userid>\d+)/(?P<page_index>\d+)/$', 'author', name='foo_blog_author'),
                       url(r'^category/(?P<slug>[-\w]+)/$', 'category', { 'page_index':0 }, name='foo_blog_category'),
                       url(r'^category/(?P<slug>[-\w]+)/(?P<page_index>\d+)/$', 'category', name='foo_blog_category'),
                       url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'post', name='foo_blog_post'),
                       url(r'^sitemap.xml$', 'sitemap'),                       
)

urlpatterns += patterns('', 
                      url(r'^xmlrpc/$', 'django_xmlrpc.views.handle_xmlrpc'), # MetaWeblog API methods
                      )


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
