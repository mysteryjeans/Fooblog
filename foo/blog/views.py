'''
Views for blogging engine

Copyright 2012 Faraz Masood Khan, mk.faraz@gmail.com
'''

from django.http import Http404
from django.template import RequestContext
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response 

from foo.settings import PAGE_SIZE
from foo.blog import PUBLISHED
from foo.blog.models import Post, Category, Author



def index(request, page_index):
    '''Return published posts'''
    
    page_index = int(page_index)
    posts = get_page(Post.latest(), page_index)
    
    prev_url = reverse('foo_blog_index', args=[page_index + 1]) if len(posts) == PAGE_SIZE else None
    next_url = reverse('foo_blog_index', args=[page_index - 1]) if page_index else None
    return render_response(request, 'blog/index.html', locals())


def author(request, userid, page_index):
    '''Return blog posts of author'''
    
    page_index = int(page_index)
    author = get_object_or_404(Author, id=int(userid))
    page_title = posts_title = 'Posts By ' + unicode(author)
    posts = get_page(Post.latest().filter(author=author), page_index)
    
    prev_url = reverse('foo_blog_author', args=[userid, page_index + 1]) if len(posts) == PAGE_SIZE else None
    next_url = reverse('foo_blog_author', args=[userid, page_index - 1]) if page_index else None
    
    return render_response(request, 'blog/index.html', locals())


def tag(request, tag, page_index):
    '''Return blog posts containing tag'''
    
    page_index = int(page_index)
    page_title = posts_title = 'Tag  ' + tag
    posts = get_page(Post.latest().filter(tags__icontains=tag), page_index)
    
    prev_url = reverse('foo_blog_tag', args=[tag, page_index + 1]) if len(posts) == PAGE_SIZE else None
    next_url = reverse('foo_blog_tag', args=[tag, page_index - 1]) if page_index else None
    
    return render_response(request, 'blog/index.html', locals())


def category(request, slug, page_index):
    '''Return posts in that category'''
    
    page_index = int(page_index)
    category = Category.objects.get(slug=slug)
    page_title = posts_title = 'Category ' + category.name
    posts = get_page(Post.latest().filter(categories=category), page_index)
    
    prev_url = reverse('foo_blog_category', args=[slug, page_index + 1]) if len(posts) == PAGE_SIZE else None
    next_url = reverse('foo_blog_category', args=[slug, page_index - 1]) if page_index else None
    
    return render_response(request, 'blog/index.html', locals())


def post(request, year, month, day, slug):
    '''Show blog post'''
    
    post = Post.read(slug)
    if post.status != PUBLISHED and not request.user.is_authenticated():
        raise Http404()
    
    page_title = post.title
    meta_keywords = post.tags
    meta_description = Truncator(strip_tags(post.content)).words(40)
    return render_response(request, 'blog/post.html', locals())


def sitemap(request):
    site = Site.objects.get_current()
    posts = Post.latest()[:100]
    r = render_response(request, 'blog/sitemap.xml', locals())
    r['Content-Type'] = 'text/xml; charset=utf-8'
    return r


def get_page(query_list, page_index):
    '''Slice filter query to require page, page size is define in settings'''
    
    start_index = page_index * PAGE_SIZE
    return query_list[start_index:start_index + PAGE_SIZE]
     

def render_response(request, *args, **kwargs):
    """
    Render template using RequestContext so that context processors should be available in template
    """
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)