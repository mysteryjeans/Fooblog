'''
Blog models administrations module

Copyright 2012 Faraz Masood Khan, mk.faraz@gmail.com
'''

from django.contrib import admin

from foo.blog.models import Author, Post, Category, Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'file',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_on', 'published', 'author', 'impressions')
    list_filter = ('published', 'created_on', 'featured', 'status',)
    date_hierarchy = 'published'
    prepopulated_fields = {'slug' : ('title',)}
    ordering = ('-created_on',)
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on', 'featured',)
    list_filter = ('featured', 'created_on',)
    prepopulated_fields = {'slug' : ('name',)}
    ordering = ('name',)


admin.site.register(Image, ImageAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)

