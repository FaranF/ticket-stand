from collections.abc import Iterator
from typing import Any
from django.contrib import admin
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models
from datetime import date, timedelta


# Register your models here.


class RatingFilter(admin.SimpleListFilter):
    title = "rating"
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return [
            ("<5", "Lower than 5"),
            ("5-6", "5-6"),
            ("6-7", "6-7"),
            ("7-8", "7-8"),
            ("8-9", "8-9"),
            ("9-10", "9-10"),
            ("10", "10"),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<5":
            return queryset.filter(rating__lt=5)
        elif self.value() == "5-6":
            return queryset.filter(rating__range=(5, 6))
        elif self.value() == "6-7":
            return queryset.filter(rating__range=(5, 6))
        elif self.value() == "7-8":
            return queryset.filter(rating__range=(5, 6))
        elif self.value() == "8-9":
            return queryset.filter(rating__range=(5, 6))
        elif self.value() == "9-10":
            return queryset.filter(rating__range=(5, 6))
        elif self.value() == "10":
            return queryset.filter(rating=10)


class TotalTimeFilter(admin.SimpleListFilter):
    title = "total time"
    parameter_name = "total_time"

    def lookups(self, request, model_admin):
        return [
            ("<1h", "Lower than 1 hour"),
            ("1-2h", "1 to 2 hours"),
            ("2-3h", "2 to 3 hours"),
            ("3-4h", "3 to 4 hours"),
            (">4h", "more than 4 hours"),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<1h":
            return queryset.filter(total_time__lt=timedelta(hours=1))
        elif self.value() == "1-2h":
            return queryset.filter(
                total_time__range=(timedelta(hours=1), timedelta(hours=2))
            )
        elif self.value() == "2-3h":
            return queryset.filter(
                total_time__range=(timedelta(hours=2), timedelta(hours=3))
            )
        elif self.value() == "3-4h":
            return queryset.filter(
                total_time__range=(timedelta(hours=3), timedelta(hours=4))
            )
        elif self.value() == ">4h":
            return queryset.filter(total_time__gt=timedelta(hours=4))


class ReleaseDateFilter(admin.SimpleListFilter):
    title = "release date"
    parameter_name = "release_date"

    def lookups(self, request, model_admin):
        return [
            ("<1990", "Before 1990"),
            ("1990-1994", "1990 to 1994"),
            ("1995-1999", "1995 to 1999"),
            ("2000-2004", "2000 to 2004"),
            ("2005-2009", "2005 to 2009"),
            ("2010-2014", "2010 to 2014"),
            ("2015-2019", "2015 to 2019"),
            ("2020-2023", "2020 to 2023"),
            (">2024", "After 2024"),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<1990":
            return queryset.filter(release_date__lt=date(1990, 1, 1))
        elif self.value() == "1990-1994":
            return queryset.filter(
                release_date__range=(date(1990, 1, 1), date(1994, 12, 31))
            )
        elif self.value() == "1995-1999":
            return queryset.filter(
                release_date__range=(date(1995, 1, 1), date(1999, 12, 31))
            )
        elif self.value() == "2000-2004":
            return queryset.filter(
                release_date__range=(date(2000, 1, 1), date(2004, 12, 31))
            )
        elif self.value() == "2005-2009":
            return queryset.filter(
                release_date__range=(date(2005, 1, 1), date(2009, 12, 31))
            )
        elif self.value() == "2010-2014":
            return queryset.filter(
                release_date__range=(date(2010, 1, 1), date(2014, 12, 31))
            )
        elif self.value() == "2015-2019":
            return queryset.filter(
                release_date__range=(date(2015, 1, 1), date(2019, 12, 31))
            )
        elif self.value() == "2020-2023":
            return queryset.filter(
                release_date__range=(date(2020, 1, 1), date(2023, 12, 31))
            )
        elif self.value() == ">2024":
            return queryset.filter(release_date__gt=date(2023, 12, 31))


class AgeFilter(admin.SimpleListFilter):
    title = "age"
    parameter_name = "age"

    def lookups(self, request, model_admin):
        return [
            ("0-12", "0-12 (Child Actors)"),
            ("13-17", "13-17 (Teen Actors)"),
            ("18-24", "18-24 (Young Adult Actors)"),
            ("25-54", "25-54 (Adult Actors)"),
            ("55+", "55+ (Senior Actors)"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "0-12":
            return queryset.filter(age__lte=12)
        elif self.value() == "13-17":
            return queryset.filter(age__range=(13, 17))
        elif self.value() == "18-24":
            return queryset.filter(age__range=(18, 24))
        elif self.value() == "25-54":
            return queryset.filter(age__range=(25, 54))
        elif self.value() == "55+":
            return queryset.filter(age__gte=55)


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    autocomplete_fields = ["featured_movies", "featured_tvshows"]
    list_display = ["title", "movies_count", "tvshows_count"]
    search_fields = ["title"]

    @admin.display(ordering=["movies_count"])
    def movies_count(self, genre):
        url = (
            reverse("admin:cinema_movie_changelist")
            + "?"
            + urlencode({"genre__id": str(genre.id)})
        )
        return format_html('<a href="{}">{} Movies</a>', url, genre.movies_count)

    @admin.display(ordering=["tvshows_count"])
    def tvshows_count(self, genre):
        url = (
            reverse("admin:cinema_tvshow_changelist")
            + "?"
            + urlencode({"genre__id": str(genre.id)})
        )
        return format_html('<a href="{}">{} TVShows</a>', url, genre.tvshows_count)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                movies_count=Count("movies_genre", distinct=True),
                tvshows_count=Count("tvshows_genre", distinct=True),
            )
        )


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    autocomplete_fields = ["genre"]
    search_fields = ["title"]
    list_display = [
        "title",
        "rating",
        "release_date",
        "total_time",
        "r_rated",
        "status",
        "display_genres",
    ]
    list_editable = ["status"]
    list_per_page = 10
    list_filter = [
        "genre",
        RatingFilter,
        ReleaseDateFilter,
        TotalTimeFilter,
        "r_rated",
        "status",
    ]
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("genre")

    def display_genres(self, obj):
        return ", ".join([genre.title for genre in obj.genre.all()])


@admin.register(models.TVShow)
class TVShowAdmin(admin.ModelAdmin):
    autocomplete_fields = ["genre"]
    search_fields = ["title"]
    list_display = [
        "title",
        "rating",
        "release_date",
        "finish_date",
        "season_count",
        "r_rated",
        "status",
        "display_genres",
    ]
    list_editable = ["status"]
    list_per_page = 10
    list_filter = [
        "genre",
        RatingFilter,
        ReleaseDateFilter,
        "r_rated",
        "status",
    ]
    
    @admin.display(ordering=["season_count"])
    def season_count(self, tvshow):
        url = (
            reverse("admin:cinema_season_changelist")
            + "?"
            + urlencode({"tvshow__id": str(tvshow.id)})
        )
        return format_html('<a href="{}">{} Seasons</a>', url, tvshow.season_count)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                season_count=Count("season_tvshow"),
            ).prefetch_related("genre")
        )
    
    def display_genres(self, obj):
        return ", ".join([genre.title for genre in obj.genre.all()])
    
    def lookup_allowed(self, key):
        return True


@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
    autocomplete_fields = ["tvshow"]
    search_fields = ["title"]
    list_display = [
        "title",
        "rating",
        "release_date",
        "episode_count",
    ]
    list_select_related = ["tvshow"]
    list_filter = [
        RatingFilter,
        ReleaseDateFilter,
        "tvshow",
    ]
    
    @admin.display(ordering=["episode_count"])
    def episode_count(self, season):
        url = (
            reverse("admin:cinema_episode_changelist")
            + "?"
            + urlencode({"season__id": str(season.id)})
        )
        return format_html('<a href="{}">{} Episodes</a>', url, season.episode_count)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                episode_count=Count("episode_season", distinct=True),
            )
        )


@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
    autocomplete_fields = ["season"]
    search_fields = ["title"]
    list_display = [
        "title",
        "rating",
        "total_time",
        "episode_number",
    ]
    list_select_related = ["season"]
    list_filter = [
        RatingFilter,
        "season",
    ]


@admin.register(models.Cast)
class CastAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name"]
    list_display = [
        "fullname",
        "age",
    ]
    list_per_page = 20
    list_filter = [
        AgeFilter,
    ]

    def fullname(self, cast: models.Cast):
        return f"{cast.first_name} {cast.last_name}"


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    autocomplete_fields = ["cast"]
    search_fields = ["role_name"]
    list_display = [
        "role_name",
        "cast_fullname",
        "get_related_title",
    ]
    list_select_related = ["cast", "content_type"]

    def cast_fullname(self, role: models.Role):
        return f"{role.cast.first_name} {role.cast.last_name}"

    def get_related_title(self, role: models.Role):
        if role.content_type.model in ["movie", "tvshow"]:
            return role.content_type.model_class().objects.get(pk=role.object_id).title

@admin.register(models.Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    search_fields = ["user__first_name", "user__last_name"]
    list_display = [
        "user_id",
        "first_name",
        "last_name",
        "picture",
        "average_rating",
    ]
    list_per_page = 20
    list_select_related = ["user"]
    ordering = ["user__first_name", "user__last_name"]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    autocomplete_fields = ["reviewer"]
    search_fields = ["reviewer__user__first_name", "reviewer__user__last_name", "text"]
    list_per_page = 10
    list_display = [
        "created_at",
        "reviewer",
        "get_related_title",
        "text",
    ]
    list_filter = [
        "created_at",
    ]
    
    def get_related_title(self, role: models.Role):
        if role.content_type.model in ["movie", "tvshow"]:
            return role.content_type.model_class().objects.get(pk=role.object_id).title
