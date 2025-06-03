from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FavoriteAPIView, RecipeViewSet

router_v1 = DefaultRouter()
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('recipes/', include('api.shopping_cart.urls')),
    path('recipes/', include('api.short_urls.urls')),
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteAPIView.as_view(), name='favorite'),
    path('', include(router_v1.urls)),
]
