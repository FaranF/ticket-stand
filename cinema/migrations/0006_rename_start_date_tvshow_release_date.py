# Generated by Django 5.0.1 on 2024-01-30 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0005_rename_season_episode_season'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tvshow',
            old_name='start_date',
            new_name='release_date',
        ),
    ]