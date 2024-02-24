from functools import lru_cache

from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tag, Ingredient, Recipe
from core.models import Follow
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeSerialzier, FollowSerializer
)
from .filters import RecipeFilter

from django.db.models import Q



class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',) 


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerialzier
    filter_backends = (DjangoFilterBackend,)
    filterset_class  = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author_write=self.request.user)




class FollowViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
    serializer_class = FollowSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
