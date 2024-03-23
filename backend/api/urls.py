from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .recipe.views import IngredientViewSet, RecipeViewSet, TagViewSet
from .users.views import subscribe, SubscriptionsViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    # будет вставляться промежуточный /version_2/
    path('', include(router_v1.urls)),
    path('users/<int:follow_id>/subscribe/', subscribe),
    path('users/subscriptions/', SubscriptionsViewSet.as_view(
        {'get': 'list'})),
]
