'''
Context processors for blog app

Copyright 2012 Faraz Masood Khan, mk.faraz@gmail.com
'''

from foo import settings
from foo.blog.models import Category, Post

def bootstrip(request):
    return {
    'featured_categories': Category.objects.filter(featured=True)[:5],
    'top_posts': Post.top()[:7],
    'site_name': settings.SITE_NAME,
    'site_meta_keywords': settings.META_KEYWORDS,
    'site_meta_description': settings.META_DESCRIPTION
    }