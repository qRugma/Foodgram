from django.urls import include, path
# from rest_framework.routers import DefaultRouter
from .views import subscribe, subscriptions, favorite, cart


# router = DefaultRouter()
app_name = 'users'

# router.register('(?P<user_id>\d+)/subscribe', FollowViewSet)

urlpatterns = [
    # path('users/', include(router.urls)),
    path('users/<int:follow_id>/subscribe/', subscribe),
    path('recipes/<int:recipe_id>/favorite/', favorite),
    path('recipes/<int:recipe_id>/shopping_cart/', cart),
    path('users/subscriptions/', subscriptions.as_view({'get': 'list'})),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
