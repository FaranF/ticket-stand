from django_filters.rest_framework import FilterSet
from . import models

class MovieFilter(FilterSet):
  class Meta:
    model = models.Movie
    fields = {
      'genre_id': ['exact'],
      'rating': ['gt', 'lt'],
      'total_time': ['gt', 'lt'],
      'status': ['exact'],
      'release_date': ['gt', 'lt'],
    }
    
class TVShowFilter(FilterSet):
  class Meta:
    model = models.TVShow
    fields = {
      'genre_id': ['exact'],
      'rating': ['gt', 'lt'],
      'status': ['exact'],
      'release_date': ['gt', 'lt'],
    }
    
class SeasonFilter(FilterSet):
  class Meta:
    model = models.Season
    fields = {
      'tvshow_id': ['exact'],
      'rating': ['gt', 'lt'],
      'release_date': ['gt', 'lt'],
    }
    
class EpisodeFilter(FilterSet):
  class Meta:
    model = models.Episode
    fields = {
      'season_id': ['exact'],
      'rating': ['gt', 'lt'],
    }
    
class CastFilter(FilterSet):
  class Meta:
    model = models.Cast
    fields = {
      'age': ['gt', 'lt'],
    }
    
class RoleFilter(FilterSet):
  class Meta:
    model = models.Role
    fields = {
      'cast_id': ['exact'],
    }