from django.contrib import admin
from .models import User, Article, Comment, Like

# Register your models here.
admin.site.register(User)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Like)
