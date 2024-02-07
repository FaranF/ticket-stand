from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("lists", views.ListViewSet, basename="lists")
# router.register("listitems", views.ListItemViewSet, basename="listitems")

lists_router = routers.NestedDefaultRouter(router, "lists", lookup="lists")
lists_router.register("items", views.ListItemViewSet, basename="list-items")


# URLConf
urlpatterns = (
    router.urls
    + lists_router.urls
)
