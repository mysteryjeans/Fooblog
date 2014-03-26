'''
Models for blogging engine

@copyright: Copyright 2012 Faraz Masood Khan, mk.faraz@gmail.com
@author: Faraz Masood Khan
'''

import re
import datetime

from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse

from foo.blog import DRAFT, WITHDRAWN, PUBLISHED


class Image(models.Model):
    '''Image uploads'''
    title = models.CharField(max_length=255)
    file = models.ImageField(upload_to='images')
    
    def __unicode__(self):
        return self.title    


class Author(User):
    '''Author of blog post'''

    def __unicode__(self):
        if self.first_name and self.last_name:
            return u'%s %s' % (self.first_name, self.last_name)
        return self.username

    @models.permalink
    def get_absolute_url(self):
        '''Return author's URL'''
        return ('foo_blog_author', (self.id,))

    class Meta:
        '''Author's Meta'''
        proxy = True


class Category(models.Model):
    '''Category for posts'''
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    featured = models.BooleanField(default=False, help_text='Should be displayed')
    description = models.TextField(blank=True)
    created_on = models.DateTimeField('creation date', auto_now=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'
    
    def __unicode__(self):
        return unicode(self.name)
    
    @models.permalink
    def get_absolute_url(self):
        '''Returns category url'''
        return ('foo_blog_category', (self.slug,))


class Post(models.Model):
    '''A Blog post'''
    
    IMG_SRC_REGEX = re.compile(r'<img[^>]*src\s*=\s*"([^"\r\n]+)"[^>]*>')
    
    STATUSES = ((DRAFT, 'Draft'),
                (WITHDRAWN, 'Withdrawn'),
                (PUBLISHED, 'Published'),)
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255,
                            help_text='Title text to be used in url for this post')
    content = models.TextField()
    excerpt = models.TextField(blank=True,
                               help_text='Content excerpt (optional)')
    status = models.CharField(max_length=1, choices=STATUSES, default=DRAFT)    
    tags = models.CharField(max_length=255, blank=True)
    categories = models.ManyToManyField(Category, verbose_name='categories', related_name='posts', blank=True, null=True)
    related = models.ManyToManyField('self', verbose_name='related posts', blank=True, null=True)
    featured = models.BooleanField('Featured', default=False)
    impressions = models.IntegerField(default=0)
    comment_enabled = models.BooleanField('comment enabled', default=True)
    author = models.ForeignKey(Author)
    published = models.DateTimeField('published date', blank=True, null=True)
    created_on = models.DateTimeField('creation date', auto_now_add=True)
    updated_on = models.DateTimeField('last updated', auto_now=True)
    
    def __unicode__(self):
        return unicode(self.title)
    
    def is_published(self):
        return self.status == PUBLISHED
    
    def preview_img_url(self):
        '''Return image for preview from HTML content (if available)'''
        try:            
            return Post.IMG_SRC_REGEX.search(self.content).groups()[0]
        except:            
            return None
        
    def plain_content(self):
        r'''
        Strips all tags from HTML content but converts </p> and <br/> to new line characters
        
        </p> == \n\n        
        <br> == \n
        
        Use linebreaks filter in templates to convert new line characters into </p> and <br/> respectively
        '''
        plain_text = re.sub(r'<\s*/p\s*>', '\n\n', unicode(self.content))
        plain_text = re.sub(r'<\s*(br)\s*?/>', '\n', plain_text)
        return strip_tags(plain_text)
    
    def tag_list(self):        
        return [(tag.strip(), reverse('foo_blog_tag', args=[tag.strip()])) for tag in self.tags.split(',')]
    
    @models.permalink
    def get_absolute_url(self):
        '''Returns post url'''
        return ('foo_blog_post', (self.published.year, self.published.month, self.published.day, self.slug),)
    
    @classmethod
    def latest(cls):
        return cls.objects.filter(status=PUBLISHED).order_by('-published')
    
    @classmethod
    def top(cls):
        from_date = datetime.datetime.now().date() - datetime.timedelta(days=14)
        return cls.objects.filter(status=PUBLISHED,published__gt=from_date).order_by('-impressions')
    
    @classmethod
    def read(cls, slug):
        post = get_object_or_404(cls, slug=slug)
        cls.objects.filter(id=post.id).update(impressions=F('impressions') + 1)
        return post



