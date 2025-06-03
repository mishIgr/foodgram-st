from django.urls import path

from .views import DownloadShoppingCartView, ShoppingCartAPIView

urlpatterns = [
    path(
        '<int:recipe_id>/shopping_cart/',
        ShoppingCartAPIView.as_view(),
        name='shopping_cart'
    ),
    path(
        'download_shopping_cart/',
        DownloadShoppingCartView.as_view(),
        name='download_shopping_cart'
    ),
]
