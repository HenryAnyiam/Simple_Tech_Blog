# Generated by Django 4.2.10 on 2024-02-26 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0017_user_mini_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='summary',
        ),
    ]