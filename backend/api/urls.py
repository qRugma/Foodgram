from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet, IngredientViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('tag', TagViewSet)
router.register('ingredient', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
