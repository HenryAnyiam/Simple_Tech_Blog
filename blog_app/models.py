from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.utils import timezone
from PIL import Image
from os import path, remove
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    """map to table user"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    about = models.TextField(null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True)
    mini_thumbnail = models.ImageField(upload_to='thumbnails', blank=True)
    confirmed_email = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'User: {self.email} {self.username}'
    
    def clear_older_images(self):
        """clear older images before setting a new one"""
        if self.profile_pic and path.isfile(self.profile_pic.path):
            remove(self.profile_pic.path)
        if self.thumbnail and path.isfile(self.thumbnail.path):
            remove(self.thumbnail.path)
        if self.mini_thumbnail and path.isfile(self.mini_thumbnail.path):
            remove(self.mini_thumbnail.path)

    
    def confirm_email(self):
        """confirm user email"""
        self.confirmed_email = True
        self.save()
    
    def get_thumbnail(self):
        """get thumbnail for image"""
        if self.profile_pic:
            image = Image.open(self.profile_pic.path)
            image = Image.Image.copy(image)
            if image.width > 200 or image.height > 200:
                image.thumbnail((300, 300))
                name = 'profile_' + path.basename(self.profile_pic.path)
                image.save(path.join(settings.MEDIA_ROOT, 'thumbnails', name))
                self.thumbnail = path.join('thumbnails', name)
                image = Image.Image.copy(image)
                image.thumbnail((30, 30))
                name ='profile_thumb_' + path.basename(self.profile_pic.path)
                image.save(path.join(settings.MEDIA_ROOT, 'thumbnails', name))
                self.mini_thumbnail = path.join('thumbnails', name)
                


class Article(models.Model):
    """map to table article"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='post_images', blank=True)
    body = models.TextField()
    publish_date = models.DateTimeField(null=True)
    views = models.PositiveIntegerField(default=0)
    edited = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True)


    def __str__(self) -> str:
        return f'{self.title} by {self.author.username}'
    
    def publish_article(self) -> None:
        """update publish article publish date"""

        if self.publish_date:
            self.edited = True
        else:
            self.publish_date = timezone.now()
        self.save()

    
    def get_thumbnail(self):
        """get thumbnail for image"""
        if self.image:
            image = Image.open(self.image)
            image = Image.Image.copy(image)
            if image.width > 200 or image.height > 200:
                image.thumbnail((300, 300))
                name = 'article_' + path.basename(self.image.path)
                image.save(path.join(settings.MEDIA_ROOT, 'thumbnails', name))
                self.thumbnail = path.join('thumbnails', name)
    
    def clear_older_images(self):
        """clear older images before setting a new one"""
        if self.image and path.isfile(self.image.path):
            remove(self.image.path)
        if self.thumbnail and path.isfile(self.thumbnail.path):
            remove(self.thumbnail.path)
    
    


class Comment(models.Model):
    """map to table comments"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self) -> str:
        return f'Comment by {self.user.username} on {self.article.title}'

class Like(models.Model):
    """map to table Like"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='likes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')

    def __str__(self) ->str:
        return f'{self.user.username} likes {self.article.title}'



class News(models.Model):
    """map to table news"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, null=False, unique=True)
    link = models.URLField(null=False)
    summary = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
