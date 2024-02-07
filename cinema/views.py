from django.shortcuts import render
from django.db.models.aggregates import Count

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from . import models, paginations, serializers, filters

# Create your views here.
class GenreViewSet(ModelViewSet):
    queryset = models.Genre.objects.annotate(
                movies_count=Count("movies_genre", distinct=True),
                tvshows_count=Count("tvshows_genre", distinct=True),
            ).all()
    serializer_class = serializers.GenreSerializer
    pagination_class = paginations.DefaultPagination
    # permission_classes = 
    search_fields = ['title']
    

class MovieViewSet(ModelViewSet):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.MovieFilter
    pagination_class = paginations.DefaultPagination
    # permission_classes = 
    search_fields = ['title', 'description']
    ordering_fields = ['rating', 'release_date', 'total_time', 'status']
    

class TVShowViewSet(ModelViewSet):
    queryset = models.TVShow.objects.annotate(
        season_count=Count('season_tvshow')).all()
    serializer_class = serializers.TVShowSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.TVShowFilter
    pagination_class = paginations.DefaultPagination
    # permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['rating', 'release_date', 'total_released_time', 'status', 'season_count']
    
    
class SeasonViewSet(ModelViewSet):
    queryset = models.Season.objects.annotate(
        episode_count=Count('episode_season')).all()
    serializer_class = serializers.SeasonSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.SeasonFilter
    pagination_class = paginations.DefaultPagination
    # permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['rating', 'release_date', 'season_count']
    
    
class EpisodeViewSet(ModelViewSet):
    queryset = models.Episode.objects.all()
    serializer_class = serializers.EpisodeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.EpisodeFilter
    pagination_class = paginations.DefaultPagination
    # permission_classes = 
    search_fields = ['title', 'description']
    ordering_fields = ['rating', 'total_time', 'episode_number']
    
    
class CastViewSet(ModelViewSet):
    queryset = models.Cast.objects.all()
    serializer_class = serializers.CastSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.CastFilter
    pagination_class = paginations.DefaultPagination
    # permission_classes = 
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['age']
    
    
class RoleViewSet(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.RoleFilter
    pagination_class = paginations.DefaultPagination
    # permission_classes = 
    search_fields = ['role_name', 'cast__first_name', 'cast__last_name']
    ordering_fields = ['cast__age']
    
    
class ReviewerViewSet(ModelViewSet):
    queryset = models.Reviewer.objects.all()
    serializer_class = serializers.ReviewerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        reviewer = models.Reviewer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = serializers.ReviewerSerializer(reviewer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.ReviewerSerializer(reviewer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
        
class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(object_id=self.kwargs['object_id'])

    # def get_serializer_context(self):
    #     return {'object_id': self.kwargs['object_id']}

