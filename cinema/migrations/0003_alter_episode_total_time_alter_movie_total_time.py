# Generated by Django 5.0.1 on 2024-01-30 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0002_alter_movie_r_rated_alter_movie_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='total_time',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='total_time',
            field=models.DurationField(),
        ),
    ]
