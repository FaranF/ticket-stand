# Generated by Django 5.0.1 on 2024-02-05 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0009_alter_cast_picture_alter_episode_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='season',
            name='episode_count',
        ),
        migrations.RemoveField(
            model_name='tvshow',
            name='season_count',
        ),
        migrations.AlterField(
            model_name='episode',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episode_season', to='cinema.season'),
        ),
        migrations.AlterField(
            model_name='season',
            name='tvshow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_tvshow', to='cinema.tvshow'),
        ),
    ]