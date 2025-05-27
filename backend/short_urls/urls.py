from django.urls import path

from .views import ShortUrlAPIView, ShortUrlRedirectionAPIView

urlpatterns = [
    path('api/recipes/<int:recipe_id>/get-link/',
         ShortUrlAPIView.as_view(), name='get-link'),
    path('s/<str:short_url>/',
         ShortUrlRedirectionAPIView.as_view(), name='redirect'),
]
