from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet, IngredientViewSet, RecipeViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
