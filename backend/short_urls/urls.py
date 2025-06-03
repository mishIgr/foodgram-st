from django.urls import path

from .views import ShortUrlRedirectionAPIView

urlpatterns = [
    path('<str:short_url>/',
         ShortUrlRedirectionAPIView.as_view(), name='redirect'),
]
