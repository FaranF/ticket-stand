from rest_framework import serializers
from . import models
from datetime import date, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator


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
        ]

    total_released_time = serializers.SerializerMethodField(method_name="calculate_relased_time")
    genres = serializers.SerializerMethodField(method_name="genres_titles")
    season_count = serializers.IntegerField(validators=[MinValueValidator(1)])
    
    def genres_titles(self, obj):
        return ", ".join([genre.title for genre in obj.genre.all()])
    
    def calculate_relased_time(self, obj:models.TVShow):
        if obj.finish_date != None:
            return obj.finish_date - obj.release_date
        else:
            return date.today() - obj.release_date

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