'''
@copyright: Copyright Faraz Masood Khan 
@author: Faraz Masood Khan
'''

from django.conf.urls import url, patterns
from foo.feed.rss import LatestFeed

urlpatterns = patterns('',
                       url(r'^/$', LatestFeed()),                       
)