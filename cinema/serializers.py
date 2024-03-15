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
    cast = CastSerializer()
    class Meta:
        model = models.Role
        fields = [
            "id",
            "role_name",
            "cast",
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
        
    # user_id = serializers.IntegerField(read_only=True)
        
        
class CommentSerializer(serializers.ModelSerializer):
    reviewer = ReviewerSerializer()
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
        return models.Comment.objects.create(object_id=object_id, **validated_data)


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
        comments = models.Role.objects.filter(content_type__model='movie', object_id=obj.id)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

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
            "genre",
            "description",
        ]

    total_released_time = serializers.SerializerMethodField(method_name="calculate_relased_time")
    season_count = serializers.IntegerField(validators=[MinValueValidator(1)])
    # season_count = serializers.IntegerField(method_name="calculate_season_count", validators=[MinValueValidator(1)])
    
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


