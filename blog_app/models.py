from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    """map to table user"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    about = models.TextField(null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    confirmed_email = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'User: {self.email} {self.username}'
    
    def confirm_email(self):
        """confirm user email"""
        self.confirmed_email = True
        self.save()


class Article(models.Model):
    """map to table article"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='post_images', blank=True)
    body = models.TextField()
    publish_date = models.DateTimeField(null=True)
    summary = models.TextField(max_length=250, null=True)
    views = models.PositiveIntegerField(default=0)
    edited = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.title} by {self.author.username}'
    
    def publish_article(self) -> None:
        """update publish article publish date"""

        if self.publish_date:
            self.edited = True
        else:
            self.publish_date = timezone.now()
            self.get_summary()
        self.save()
    
    def get_summary(self):
        """get a default summary"""
        if len(self.body) < 200:
            length = len(self.body) // 2
            summary = self.body[:length]
        else:
            summary = self.body[:200]
        self.summary = summary


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
    title = models.CharField(max_length=250, null=False, unique=True)
    link = models.URLField(null=False)
    summary = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
