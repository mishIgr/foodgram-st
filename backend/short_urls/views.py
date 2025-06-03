from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView

from .models import ShortUrl


class ShortUrlRedirectionAPIView(APIView):

    def get(self, request, short_url):
        short_url = f'/s/{short_url}/'
        obj = get_object_or_404(ShortUrl, short_url=short_url)
        return redirect(request.build_absolute_uri(obj.origin_url))
