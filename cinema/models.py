from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Genre(models.Model):
    title = models.CharField(max_length=255)
    featured_movies = models.ForeignKey(
        'Movie', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)
    featured_tvshows = models.ForeignKey(
        'TVShow', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)
    
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
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    featured_comments = models.ForeignKey(
        'Comment', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)


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
    season_count = models.PositiveIntegerField()
    picture = models.ImageField()
    picture_background = models.ImageField()
    description = models.TextField()
    r_rated = models.BooleanField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    featured_seasons = models.ForeignKey(
        'Season', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)
    featured_comments = models.ForeignKey(
        'Comment', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)
    
    
class Season(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    episode_count = models.PositiveIntegerField()
    picture = models.ImageField(null=True)
    description = models.TextField(null=True)
    tvshow = models.ForeignKey(TVShow, on_delete=models.CASCADE)
    featured_episodes = models.ForeignKey(
        'Episode', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)
    
class Episode(models.Model):
    title = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    episode_number = models.IntegerField()
    picture = models.ImageField(null=True)
    description = models.TextField(null=True)
    total_time = models.DurationField(null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    

class Cast(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True)
    picture = models.ImageField(null=True)
    featured_roles = models.ForeignKey(
        'Role', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)
    
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
    picture = models.ImageField(null=True)
    
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