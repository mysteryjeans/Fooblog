'''
XML-RPC methods for MetaWeblog API

Created on Oct 31, 2012

@author: Faraz Masood Khan
'''

import os
from datetime import datetime
from xmlrpclib import Fault, DateTime

from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.text import Truncator
from django.utils.html import strip_tags
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.template.defaultfilters import slugify

from django_xmlrpc.decorators import xmlrpc_func

from foo.blog import PUBLISHED, DRAFT
from foo.blog.models import Author, Post, Category


PROTOCOL = 'http'
UPLOAD_TO = getattr(settings, 'UPLOAD_TO', 'uploads/blog')

# http://docs.nucleuscms.org/blog/12#errorcodes
LOGIN_ERROR = 801
PERMISSION_DENIED = 803


def authenticate(username, password, permission=None):
    """Authenticate staff_user with permission"""
    try:
        user = Author.objects.get(username__exact=username)
    except User.DoesNotExist:
        raise Fault(LOGIN_ERROR, 'Username is incorrect.')
    if not user.check_password(password):
        raise Fault(LOGIN_ERROR, 'Password is invalid.')
    if not user.is_staff or not user.is_active:
        raise Fault(PERMISSION_DENIED, 'User account unavailable.')
    if permission:
        if not user.has_perm(permission):
            raise Fault(PERMISSION_DENIED, 'User cannot %s.' % permission)
    return user

def blog_structure(site):
    """A blog structure"""
    return {'url': '%s://%s%s' % (
            PROTOCOL, site.domain, reverse('foo_blog_index')),
            'blogid': settings.SITE_ID,
            'blogName': settings.SITE_NAME}


def user_structure(user, site):
    """An user structure"""
    return {'userid': user.pk,
            'email': user.email,
            'nickname': user.username,
            'lastname': user.last_name,
            'firstname': user.first_name,
            'url': '%s://%s%s' % (
                PROTOCOL, site.domain,
                reverse('foo_blog_author', args=[user.username]))}


def author_structure(user):
    """An author structure"""
    return {'user_id': user.pk,
            'user_login': user.username,
            'display_name': unicode(user),
            'user_email': user.email}


def category_structure(category, site):
    """A category structure"""
    return {'description': category.name,
            'htmlUrl': '%s://%s%s' % (PROTOCOL, site.domain, category.get_absolute_url()),
            'rssUrl': '%s://%s%s' % (PROTOCOL, site.domain, reverse('foo_blog_category', args=[category.slug])),
            # Useful Wordpress Extensions
            'categoryId': category.pk,            
            'categoryDescription': category.description,
            'categoryName': category.name}


def post_structure(post, site):
    """A post structure with extensions"""
    author = post.author
    return {'title': post.title,
            'description': unicode(post.content),
            'link': '%s://%s%s' % (PROTOCOL, site.domain, post.get_absolute_url()),
            # Basic Extensions
            'permaLink': '%s://%s%s' % (PROTOCOL, site.domain, post.get_absolute_url()),
            'categories': [cat.name for cat in post.categories.all()],
            'dateCreated': DateTime(post.created_on.isoformat()),
            'postid': post.pk,
            'userid': author.username,
            # Useful Movable Type Extensions
            'mt_excerpt': post.excerpt,
            'mt_allow_comments': int(post.comment_enabled),
            #'mt_allow_pings': int(entry.pingback_enabled),
            'mt_keywords': post.tags,
            # Useful Wordpress Extensions
            'wp_author': author.username,
            'wp_author_id': author.pk,
            'wp_author_display_name': unicode(author),
            #'wp_password': entry.password,
            'wp_slug': post.slug,
            'sticky': post.featured}


@xmlrpc_func(returns='struct[]', args=['string', 'string', 'string'])
def get_users_blogs(apikey, username, password):
    """blogger.getUsersBlogs(api_key, username, password)
    => blog structure[]"""
    authenticate(username, password)
    site = Site.objects.get_current()
    return [blog_structure(site)]


@xmlrpc_func(returns='struct', args=['string', 'string', 'string'])
def get_user_info(apikey, username, password):
    """blogger.getUserInfo(api_key, username, password)
    => user structure"""
    user = authenticate(username, password)
    site = Site.objects.get_current()
    return user_structure(user, site)


@xmlrpc_func(returns='struct[]', args=['string', 'string', 'string'])
def get_authors(apikey, username, password):
    """wp.getAuthors(api_key, username, password)
    => author structure[]"""
    authenticate(username, password)
    return [author_structure(author)
            for author in User.objects.filter(is_staff=True)]


@xmlrpc_func(returns='boolean', args=['string', 'string', 'string', 'string', 'string'])
def delete_post(apikey, post_id, username, password, publish):
    """blogger.deletePost(api_key, post_id, username, password, 'publish')
    => boolean"""
    user = authenticate(username, password, 'blog.delete_post')
    entry = Post.objects.get(id=post_id, author=user)
    entry.delete()
    return True


@xmlrpc_func(returns='struct', args=['string', 'string', 'string'])
def get_post(post_id, username, password):
    """metaWeblog.getPost(post_id, username, password)
    => post structure"""
    user = authenticate(username, password)
    site = Site.objects.get_current()
    return post_structure(Post.objects.get(id=post_id), site)


@xmlrpc_func(returns='struct[]', args=['string', 'string', 'string', 'integer'])
def get_recent_posts(blog_id, username, password, number):
    """metaWeblog.getRecentPosts(blog_id, username, password, number)
    => post structure[]"""
    user = authenticate(username, password)
    site = Site.objects.get_current()    
    return [post_structure(entry, site) for entry in Post.objects.filter(author=user)[:number]]


@xmlrpc_func(returns='struct[]', args=['string', 'string', 'string'])
def get_categories(blog_id, username, password):
    """metaWeblog.getCategories(blog_id, username, password)
    => category structure[]"""
    authenticate(username, password)
    site = Site.objects.get_current()
    return [category_structure(category, site) for category in Category.objects.all()]
    
    
@xmlrpc_func(returns='string', args=['string', 'string', 'string', 'struct'])
def new_category(blog_id, username, password, category_struct):
    """wp.newCategory(blog_id, username, password, category)
    => category_id"""
    authenticate(username, password)
    category_dict = {'name': category_struct['name'],
                     'description': category_struct['description'],
                     'slug': category_struct['slug']}   
    category = Category.objects.create(**category_dict)

    return category.pk


@xmlrpc_func(returns='string', args=['string', 'string', 'string', 'struct', 'boolean'])
def new_post(blog_id, username, password, post, publish):
    """metaWeblog.newPost(blog_id, username, password, post, publish)
    => post_id"""
    user = authenticate(username, password)
    if post.get('dateCreated'):
        creation_date = datetime.strptime(
            post['dateCreated'].value[:18], '%Y-%m-%dT%H:%M:%S')
        if settings.USE_TZ:
            creation_date = timezone.make_aware(
                creation_date, timezone.utc)
    else:
        creation_date = timezone.now()

    entry_dict = {'title': post['title'],
                  'content': post['description'],
                  'excerpt': post.get('mt_excerpt', Truncator(strip_tags(post['description'])).words(50, '...')),
                  'created_on': creation_date,
                  'published': creation_date,
                  'updated_on': creation_date,
                  'comment_enabled': post.get('mt_allow_comments', 1) == 1,
                  #'pingback_enabled': post.get('mt_allow_pings', 1) == 1,
                  'featured': post.get('sticky', 0) == 1,
                  'tags': 'mt_keywords' in post and post['mt_keywords'] or '',
                  'slug': 'wp_slug' in post and post['wp_slug'] or slugify(post['title'])}                  
    
    entry_dict['status'] = publish and PUBLISHED or DRAFT
    entry_dict['author'] = user
    
    entry = Post.objects.create(**entry_dict)
    
    if 'categories' in post:
        entry.categories.add(*[Category.objects.get_or_create(name=cat, slug=slugify(cat))[0] for cat in post['categories']])

    return entry.pk


@xmlrpc_func(returns='boolean', args=['string', 'string', 'string', 'struct', 'boolean'])
def edit_post(post_id, username, password, entry, publish):
    """metaWeblog.editPost(post_id, username, password, post, publish)
    => boolean"""
    user = authenticate(username, password)
    post = Post.objects.get(id=post_id)
    if entry.get('dateCreated'):
        creation_date = datetime.strptime(entry['dateCreated'].value[:18], '%Y-%m-%dT%H:%M:%S')
        if settings.USE_TZ:
            creation_date = timezone.make_aware(creation_date, timezone.utc)
    else:
        creation_date = post.created_on

    post.title = entry['title']
    post.content = entry['description']
    post.excerpt = entry.get('mt_excerpt', Truncator(strip_tags(entry['description'])).words(50, '...'))
    post.creation_date = creation_date
    post.last_update = timezone.now()
    post.comment_enabled = entry.get('mt_allow_comments', 1) == 1
    #post.pingback_enabled = entry.get('mt_allow_pings', 1) == 1
    post.featured = entry.get('sticky', 0) == 1
    post.tags = 'mt_keywords' in entry and entry['mt_keywords'] or post.tags
    post.slug = 'wp_slug' in entry and entry['wp_slug'] or slugify(entry['title'])    
    post.status = publish and PUBLISHED or DRAFT
    #post.password = post.get('wp_password', '')
    
    if 'wp_author_id' in entry and int(entry['wp_author_id']) != user.pk:
        author = User.objects.get(pk=entry['wp_author_id'])
        post.author = author

    if 'categories' in entry:
        post.categories.clear()
        post.categories.add(*[Category.objects.get_or_create(name=cat, slug=slugify(cat))[0] for cat in entry['categories']])
        
    post.save()
        
    return True


@xmlrpc_func(returns='struct', args=['string', 'string', 'string', 'struct'])
def new_media_object(blog_id, username, password, media):
    """metaWeblog.newMediaObject(blog_id, username, password, media)
    => media structure"""
    authenticate(username, password)
    path = default_storage.save(os.path.join(UPLOAD_TO, media['name']), ContentFile(media['bits'].data))
    site = Site.objects.get_current()
    mediaUrl = '%s://%s%s' % (PROTOCOL, site.domain, default_storage.url(path))        
    return {'url': mediaUrl}
