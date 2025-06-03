from django.urls import path

from .views import ShortUrlAPIView

urlpatterns = [
    path('<int:recipe_id>/get-link/',
         ShortUrlAPIView.as_view(), name='get-link'),
]
