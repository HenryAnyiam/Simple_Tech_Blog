# Generated by Django 4.2.10 on 2024-02-19 09:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0008_alter_like_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]