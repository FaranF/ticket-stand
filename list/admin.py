from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models.aggregates import Count
from . import models

# Register your models here.

@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):
    search_fields = ["title", "description"]
    list_per_page = 20
    list_display = [
        "id",
        "title",
        "created_at",
        "list_type",
        "description",
        "user_id",
        
    ]
    list_filter = [
        "created_at",
        "list_type",
    ]
        

@admin.register(models.ListItems)
class ListItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ["list"]
    search_fields = ["list__title"]
    list_per_page = 10
    list_display = [
        "id",
        "list_title",
        "get_related_title",
    ]
    list_select_related=["list", "content_type"]

    def get_related_title(self, list: models.List):
        return list.content_type.model_class().objects.get(pk=list.object_id).title
    
    
