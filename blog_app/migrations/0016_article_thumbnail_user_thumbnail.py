# Generated by Django 4.2.7 on 2024-02-25 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0015_alter_news_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='thumbnails'),
        ),
        migrations.AddField(
            model_name='user',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='thumbnails'),
        ),
    ]