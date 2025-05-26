from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import ShoppingCart
from short_urls.serializers import ShortRecipeSerializer


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('recipe', 'user'),
                message='Рецепт уже добавлен в корзину',
            )
        ]

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe, context=self.context
        ).data
