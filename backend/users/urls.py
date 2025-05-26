from django.urls import path, include

from .views import AvatarView


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/me/avatar/', AvatarView.as_view()),
    path('', include('subscriptions.urls')),
    path('', include('djoser.urls')),
]
