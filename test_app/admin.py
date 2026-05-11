from django.contrib import admin

from test_app.models import Book, Author, Post

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Post)
