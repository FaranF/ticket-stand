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


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = [
            "id",
            "role_name",
            "cast",
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
            "roles",
        ]
    roles = serializers.SerializerMethodField(method_name="get_roles")
    def get_roles(self, obj):
        print(obj)
        roles = models.Role.objects.filter(cast_id=obj.id)
        serializer = RoleSerializer(roles, many=True)
        return serializer.data
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            "id",
            "created_at",
            "text",
            "reviewer",
        ]
    def create(self, validated_data):
        object_id = self.context['object_id']
        content_type_id = self.context['content_type_id']
        return models.Comment.objects.create(object_id=object_id, content_type_id=content_type_id, **validated_data)
        
        
class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviewer
        fields = [
            "id",
            "average_rating",
            "user",
            "picture",
            "comments",
        ]
    comments = serializers.SerializerMethodField(method_name="get_comments")
    def get_comments(self, obj):
        comments = models.Comment.objects.filter(reviewer_id=obj.id)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data
    # user_id = serializers.IntegerField(read_only=True)

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
            "genre",
            "description",
            "roles",
            "comments"
        ]
    
    genre = serializers.PrimaryKeyRelatedField(queryset=models.Genre.objects.all(), many=True)
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['genre'] = [genre.title for genre in instance.genre.all()]
        return data
    
    roles = serializers.SerializerMethodField(method_name="get_roles")
    def get_roles(self, obj):
        roles = models.Role.objects.filter(content_type__model='movie', object_id=obj.id)
        serializer = RoleSerializer(roles, many=True)
        return serializer.data

    comments = serializers.SerializerMethodField(method_name="get_comments")
    def get_comments(self, obj):
        comments = models.Comment.objects.filter(content_type__model='movie', object_id=obj.id)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data


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
    season = serializers.PrimaryKeyRelatedField(read_only=True)
        
    def create(self, validated_data):
        season_id = self.context['season_id']
        return models.Episode.objects.create(season_id=season_id, **validated_data)


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
            "episodes",
            "tvshow",
        ]
    tvshow = serializers.PrimaryKeyRelatedField(read_only=True)

    episode_count = serializers.IntegerField(validators=[MinValueValidator(1)], read_only=True)
    episodes = serializers.SerializerMethodField(method_name="get_episodes")
    def get_episodes(self, obj):
        seasons = models.Episode.objects.filter(season_id=obj.id)
        serializer = EpisodeSerializer(seasons, many=True)
        return serializer.data
    
    def create(self, validated_data):
        tvshow_id = self.context['tvshow_id']
        return models.Season.objects.create(tvshow_id=tvshow_id, **validated_data)


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
            "seasons",
            "status",
            "genre",
            "description",
            "roles",
            "comments",
            
        ]

    total_released_time = serializers.SerializerMethodField(method_name="calculate_relased_time")
    season_count = serializers.IntegerField(validators=[MinValueValidator(1)], read_only=True)

    seasons = serializers.SerializerMethodField(method_name="get_seasons")
    def get_seasons(self, obj):
        seasons = models.Season.objects.filter(tvshow_id=obj.id)
        serializer = SeasonSerializer(seasons, many=True)
        return serializer.data
    
    genre = serializers.PrimaryKeyRelatedField(queryset=models.Genre.objects.all(), many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['genre'] = [genre.title for genre in instance.genre.all()]
        return data
    
    def calculate_relased_time(self, obj:models.TVShow):
        if obj.finish_date != None:
            return obj.finish_date - obj.release_date
        else:
            return date.today() - obj.release_date
    
    roles = serializers.SerializerMethodField(method_name="get_roles")
    def get_roles(self, obj):
        roles = models.Role.objects.filter(content_type__model='tvshow', object_id=obj.id)
        serializer = RoleSerializer(roles, many=True)
        return serializer.data

    comments = serializers.SerializerMethodField(method_name="get_comments")
    def get_comments(self, obj):
        comments = models.Comment.objects.filter(content_type__model='tvshow', object_id=obj.id)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data


