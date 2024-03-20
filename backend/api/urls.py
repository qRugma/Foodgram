from django.urls import include, path

from rest_framework.routers import DefaultRouter

from recipe.views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
# будет вставляться промежуточный /version_2/
    path('', include(router_v1.urls)),
]
