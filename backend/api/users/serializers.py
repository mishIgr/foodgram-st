from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.exceptions import NotAuthenticated

from subscriptions.models import Subscription

User = get_user_model()


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(allow_null=True)

    class Meta:
        model = User
        fields = ('avatar',)


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                author=obj
            ).exists()
        return False

    def to_representation(self, instance):
        if isinstance(instance, AnonymousUser):
            raise NotAuthenticated(
                {'detail': 'Authentication credentials were not provided.'},
                code=status.HTTP_401_UNAUTHORIZED
            )
        return super().to_representation(instance)

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        )
        read_only_fields = ('email',)


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        read_only_fields = ('id',)
