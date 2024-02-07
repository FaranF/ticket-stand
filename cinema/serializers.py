from django.core.validators import MinValueValidator, MaxValueValidator

from rest_framework import serializers

from datetime import date, timedelta
from . import models


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ["id", "title", "movies_count", "tvshows_count"]

    movies_count = serializers.IntegerField(read_only=True)
    tvshows_count = serializers.IntegerField(read_only=True)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = [
            "id",
            "title",
            "rating",
            "release_date",
            "total_time",
            "picture",
            "picture_background",
            "r_rated",
            "status",
            "genres",
            "description",
        ]

    genres = serializers.SerializerMethodField(method_name="genres_titles")

    def genres_titles(self, obj):
        return ", ".join([genre.title for genre in obj.genre.all()])


class TVShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TVShow
        fields = [
            "id",
            "title",
            "rating",
            "release_date",
            "total_released_time",
            "picture",
            "picture_background",
            "season_count",
            "status",
            "genres",
            "description",
        ]

    total_released_time = serializers.SerializerMethodField(method_name="calculate_relased_time")
    genres = serializers.SerializerMethodField(method_name="genres_titles")
    season_count = serializers.IntegerField(validators=[MinValueValidator(1)])
    # season_count = serializers.IntegerField(method_name="calculate_season_count", validators=[MinValueValidator(1)])
    
    def genres_titles(self, obj):
        return ", ".join([genre.title for genre in obj.genre.all()])
    
    def calculate_relased_time(self, obj:models.TVShow):
        if obj.finish_date != None:
            return obj.finish_date - obj.release_date
        else:
            return date.today() - obj.release_date
        
    # def calculate_season_count(self, obj:models.TVShow):
    #     # return obj.objects.annotate(Count("season_tvshow"))
    #     return Count("season_tvshow")

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Season
        fields = [
            "id",
            "title",
            "rating",
            "release_date",
            "picture",
            "description",
            "episode_count",
            "tvshow",
        ]
    episode_count = serializers.IntegerField(validators=[MinValueValidator(1)])
    # episode_count = serializers.IntegerField(method_name="calculate_episode_count", validators=[MinValueValidator(1)])
    
    # def calculate_episode_count(self, obj:models.Season):
    #     # return obj.objects.annotate(Count("season_tvshow"))
    #     return Count("episode_season")


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Episode
        fields = [
            "id",
            "title",
            "rating",
            "total_time",
            "picture",
            "episode_number",
            "description",
            "season",
        ]


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cast
        fields = [
            "id",
            "first_name",
            "last_name",
            "age",
            "picture",
        ]
        

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = [
            "id",
            "role_name",
            "cast",
            "content_type",
            "object_id",
            "content_object",
        ]
        
        
class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviewer
        fields = [
            "id",
            "average_rating",
            "user",
            "picture",
        ]
        
    user_id = serializers.IntegerField(read_only=True)
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            "id",
            "created_at",
            "text",
            "reviewer",
            "content_type",
            "object_id",
            "content_object",
        ]