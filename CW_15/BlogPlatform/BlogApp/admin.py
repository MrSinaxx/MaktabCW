from django.contrib import admin
from .models import Post, Author
from category.models import Category

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)
