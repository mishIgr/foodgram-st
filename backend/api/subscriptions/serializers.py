from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.users.serializers import CustomUserSerializer
from subscriptions.models import Subscription

User = get_user_model()


class CreateSubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(default=0)

    class Meta(CustomUserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar',
        )

    def get_recipes(self, obj):
        from api.recipes.serializers import ShortRecipeSerializer

        recipes = obj.recipes.all()
        request = self.context.get('request')
        recipes_limit_str = request.query_params.get('recipes_limit', None)
        if recipes_limit_str:
            recipes = recipes[:int(recipes_limit_str)]

        return ShortRecipeSerializer(
            recipes, many=True, context={'request': request}
        ).data


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('author', 'user')
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('author', 'user'),
                message='Вы уже подписаны на этого пользователя',
            )
        ]

    def validate_author(self, author):
        if self.context['request'].user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return author

    def to_representation(self, instance):
        return CreateSubscribeSerializer(
            instance.author, context=self.context
        ).data
