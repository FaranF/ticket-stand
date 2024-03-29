from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib import admin

# Create your models here.
class List(models.Model):
    LIST_FAVORITE = 'F'
    LIST_WATCHLIST = 'W'
    LIST_OTHER = 'O'
    LIST_CHOICES = [
        (LIST_FAVORITE, 'Favorites'),
        (LIST_WATCHLIST, 'Watchlist'),
        (LIST_OTHER, 'Other'),
    ]

    title = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    list_type = models.CharField(
        max_length=1, choices=LIST_CHOICES)
    picture = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    

class ListItems(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    @admin.display(ordering='list__title')
    def list_title(self):
        return self.list.title