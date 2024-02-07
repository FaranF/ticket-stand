from django_filters.rest_framework import FilterSet
from . import models

class ListFilter(FilterSet):
  class Meta:
    model = models.List
    fields = {
      'user_id': ['exact'],
      'created_at': ['gt', 'lt'],
      'list_type':[],
    }
    
class ListItemFilter(FilterSet):
  class Meta:
    model = models.ListItems
    fields = {
      'list_id': ['exact'],
      'object_id': ['exact'],
      'content_type': [],
      'list__list_type':[],
    }