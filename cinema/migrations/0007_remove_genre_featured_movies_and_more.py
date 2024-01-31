# Generated by Django 5.0.1 on 2024-01-31 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0006_rename_start_date_tvshow_release_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='featured_movies',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='featured_tvshows',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='tvshow',
            name='genre',
        ),
        migrations.AddField(
            model_name='genre',
            name='featured_movies',
            field=models.ManyToManyField(blank=True, related_name='featured_movies_genre', to='cinema.movie'),
        ),
        migrations.AddField(
            model_name='genre',
            name='featured_tvshows',
            field=models.ManyToManyField(blank=True, related_name='featured_tvshows_genre', to='cinema.tvshow'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(related_name='movies_genre', to='cinema.genre'),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='genre',
            field=models.ManyToManyField(related_name='tvshows_genre', to='cinema.genre'),
        ),
    ]
