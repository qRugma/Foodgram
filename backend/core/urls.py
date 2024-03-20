from django.urls import include, path

from .views import subscribe, SubscriptionsViewSet

app_name = 'users'


urlpatterns = [
    path('users/<int:follow_id>/subscribe/', subscribe),
    path('users/subscriptions/', SubscriptionsViewSet.as_view({'get': 'list'})),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
