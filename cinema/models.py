from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Genre(models.Model):
    title = models.CharField(max_length=255)
    featured_movies = models.ManyToManyField(
        'Movie', related_name="featured_movies_genre", blank=True)
    featured_tvshows = models.ManyToManyField(
        'TVShow', related_name="featured_tvshows_genre", blank=True)
    
    class Meta:
        ordering = ['title']

class Movie(models.Model):
    STATUS_RELEASED = 'R'
    STATUS_INPRODUCTION = 'P'
    STATUS_CHOICES = [
        (STATUS_RELEASED, 'Released'),
        (STATUS_INPRODUCTION, 'In Production'),
    ]

    title = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    release_date = models.DateField()
    total_time = models.DurationField()
    picture = models.ImageField()
    picture_background = models.ImageField()
    description = models.TextField()
    r_rated = models.BooleanField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    genre = models.ManyToManyField(Genre, related_name="movies_genre")


class TVShow(models.Model):
    STATUS_RELEASED = 'R'
    STATUS_INPRODUCTION = 'P'
    STATUS_CANCELED = 'C'
    STATUS_CHOICES = [
        (STATUS_RELEASED, 'Released'),
        (STATUS_INPRODUCTION, 'In Production'),
        (STATUS_CANCELED, 'Canceled'),
    ]
    
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    finish_date = models.DateField()
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    picture = models.ImageField()
    picture_background = models.ImageField()
    description = models.TextField()
    r_rated = models.BooleanField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    genre = models.ManyToManyField(Genre, related_name="tvshows_genre")
    
class Season(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    picture = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tvshow = models.ForeignKey(TVShow, on_delete=models.CASCADE, related_name="season_tvshow")

    
class Episode(models.Model):
    title = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    episode_number = models.IntegerField()
    picture = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    total_time = models.DurationField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episode_season")
    

class Cast(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Role(models.Model):
    role_name = models.CharField(max_length=255)
    cast = models.ForeignKey(Cast, on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Reviewer(models.Model):
    average_rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
    
class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()