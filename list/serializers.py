from rest_framework import serializers
from . import models
from datetime import date, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.List
        fields = [
            "id",
            "title",
            "created_at",
            "list_type",
            "picture",
            "description",
            "user",
        ]
        
class ListItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ListItems
        fields = [
            "id",
            "list",
            "content_type",
            "object_id",
            "content_object",
        ]