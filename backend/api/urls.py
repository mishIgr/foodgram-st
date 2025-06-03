from django.urls import include, path

urlpatterns = [
    path('', include('api.users.urls')),
    path('', include('api.ingredients.urls')),
    path('', include('api.recipes.urls')),
]
