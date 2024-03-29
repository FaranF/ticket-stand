from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("movies", views.MovieViewSet, basename="movies")
router.register("tvshows", views.TVShowViewSet, basename="tvshows")
router.register("casts", views.CastViewSet, basename="casts")
router.register("reviewers", views.ReviewerViewSet, basename="reviewers")

movies_router = routers.NestedDefaultRouter(router, "movies", lookup="movies")
movies_router.register("roles", views.RoleViewSet, basename="movie-roles")
movies_router.register("comments", views.CommentViewSet, basename="movie-comments")

tvshows_router = routers.NestedDefaultRouter(router, "tvshows", lookup="tvshows")
tvshows_router.register("seasons", views.SeasonViewSet, basename="tvshow-seasons")
tvshows_router.register("roles", views.RoleViewSet, basename="tvshow-roles")
tvshows_router.register("comments", views.CommentViewSet, basename="tvshow-comments")

seasons_router = routers.NestedDefaultRouter(tvshows_router, "seasons", lookup="seasons")
seasons_router.register("episodes", views.EpisodeViewSet, basename="season-episodes")

# casts_router = routers.NestedDefaultRouter(router, "casts", lookup="casts")
# casts_router.register("roles", views.RoleViewSet, basename="cast-roles")

# reviewers_router = routers.NestedDefaultRouter(router, "reviewers", lookup="reviewers")
# reviewers_router.register("comments", views.CommentViewSet, basename="reviewer-comments")

# URLConf
urlpatterns = (
    router.urls
    # + genres_router.urls
    + movies_router.urls
    + tvshows_router.urls
    + seasons_router.urls
    # + casts_router.urls
    # + reviewers_router.urls
)
