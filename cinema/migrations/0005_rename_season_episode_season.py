# Generated by Django 5.0.1 on 2024-01-30 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0004_genre_featured_movies_genre_featured_tvshows'),
    ]

    operations = [
        migrations.RenameField(
            model_name='episode',
            old_name='Season',
            new_name='season',
        ),
    ]
