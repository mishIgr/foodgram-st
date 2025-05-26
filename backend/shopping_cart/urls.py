from django.urls import path

from .views import ShoppingCartAPIView, DownloadShoppingCartView


urlpatterns = [
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingCartAPIView.as_view(),
        name='shopping_cart'
    ),
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCartView.as_view(),
        name='download_shopping_cart'
    ),
]
