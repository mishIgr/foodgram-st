from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SubscriptionsListViewSet, SubscriptionsAPIView


router_v1 = DefaultRouter()
router_v1.register(r'users/subscriptions',
                   SubscriptionsListViewSet, basename='subscriptions')

urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'users/<int:author_id>/subscribe/',
        SubscriptionsAPIView.as_view(),
        name='subscribe'
    ),
]
