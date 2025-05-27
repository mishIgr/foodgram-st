from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ShortUrl


class ShortUrlAPIView(APIView):

    def get(self, request, recipe_id):
        origin_url = f"/recipes/{recipe_id}/"
        short_url_instance, _ = ShortUrl.objects.get_or_create(
            origin_url=origin_url
        )
        return Response({
            "short-link": (request
                           .build_absolute_uri(short_url_instance.short_url))
        })


class ShortUrlRedirectionAPIView(APIView):

    def get(self, request, short_url):
        short_url = f"/s/{short_url}/"
        obj = get_object_or_404(ShortUrl, short_url=short_url)
        return redirect(request.build_absolute_uri(f"{obj.origin_url}"))
