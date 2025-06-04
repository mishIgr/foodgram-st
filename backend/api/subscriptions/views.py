from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from subscriptions.models import Subscription

from .serializers import CreateSubscribeSerializer, SubscriptionSerializer

User = get_user_model()


class SubscriptionsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateSubscribeSerializer

    def get_queryset(self):
        return User.objects.filter(
            subscribers__user=self.request.user
        ).annotate(
            recipes_count=Count('recipes')
        )


class SubscriptionsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def post(self, request, author_id):
        if not User.objects.filter(pk=author_id).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            data={'author': author_id, 'user': request.user.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, author_id):
        author = get_object_or_404(User, pk=author_id)
        deleted_count, _ = Subscription.objects.filter(
            author=author,
            user=request.user
        ).delete()

        if not deleted_count:
            return Response(
                {'detail': 'Подписка не найдена'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
