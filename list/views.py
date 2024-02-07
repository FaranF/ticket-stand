from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from . import models, serializers, filters, paginations

# Create your views here.
class ListViewSet(ModelViewSet):
    queryset = models.List.objects.all()
    serializer_class = serializers.ListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ListFilter
    pagination_class = paginations.DefaultPagination
    # permission_classes = 
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'list_type', 'user_id']


class ListItemViewSet(ModelViewSet):
    queryset = models.ListItems.objects.all()
    serializer_class = serializers.ListItemsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.ListItemFilter
    pagination_class = paginations.DefaultPagination
    # permission_classes = 
    search_fields = ['list__title']
    ordering_fields = ['list__list_type', 'list__user_id', 'object_id', 'content_type']
    