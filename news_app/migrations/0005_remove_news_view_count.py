# Generated by Django 5.0.4 on 2024-05-04 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0004_news_view_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='view_count',
        ),
    ]