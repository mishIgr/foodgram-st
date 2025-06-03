from rest_framework.response import Response
from rest_framework.views import APIView

from short_urls.models import ShortUrl


class ShortUrlAPIView(APIView):

    def get(self, request, recipe_id):
        origin_url = f'/recipes/{recipe_id}/'
        short_url_instance, _ = ShortUrl.objects.get_or_create(
            origin_url=origin_url
        )
        return Response({
            'short-link': (request
                           .build_absolute_uri(short_url_instance.short_url))
        })
