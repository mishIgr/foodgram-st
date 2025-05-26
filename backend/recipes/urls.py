from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, FavoriteAPIView

router_v1 = DefaultRouter()
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteAPIView.as_view(), name='favorite'),
]
