# Generated by Django 5.0.2 on 2024-03-15 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0010_remove_season_episode_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
