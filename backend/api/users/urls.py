from django.urls import include, path

from .views import AvatarView

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/me/avatar/', AvatarView.as_view()),
    path('', include('api.subscriptions.urls')),
    path('', include('djoser.urls')),
]
