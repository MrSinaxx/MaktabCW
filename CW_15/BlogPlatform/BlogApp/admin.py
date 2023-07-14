from calendar import c
from django.contrib import admin
from .models import Post, Author, Comment
from category.models import Category

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)
