from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.users.serializers import CustomUserSerializer
from ingredients.models import Ingredient
from recipes.models import FavoriteRecipe, Recipe, RecipeIngredient

from . import constants


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )
    amount = serializers.IntegerField(
        min_value=constants.MIN_INGREDIENT_AMOUNT)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = RecipeIngredientSerializer(
        many=True, source='recipe_ingredients'
    )
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.BooleanField(
        default=False,
        read_only=True
    )
    is_in_shopping_cart = serializers.BooleanField(
        default=False,
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('is_favorited', 'is_in_shopping_cart')

    def validate_image(self, image):
        if not image:
            raise serializers.ValidationError('Изображение обязательно.')
        return image

    def validate(self, attrs):
        ingredients = attrs.get('recipe_ingredients', [])
        if not len(ingredients):
            raise serializers.ValidationError(
                'Должен быть указан хотя бы один ингредиент.'
            )
        return super().validate(attrs)

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'Укажите хотя бы один ингредиент.'
            )

        ingredient_ids = [
            ingredient['ingredient']['id'] for ingredient in ingredients
        ]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться.'
            )

        existing_ids = set(Ingredient.objects.values_list('id', flat=True))

        missing_ids = set(ingredient_ids) - existing_ids

        if missing_ids:
            raise serializers.ValidationError(
                f'Ингредиенты с id {", ".join(map(str, missing_ids))} '
                'не найдены.',
            )
        return ingredients

    def _save_ingredients(self, recipe, ingredients_data):
        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    recipe=recipe,
                    ingredient_id=item['ingredient']['id'],
                    amount=item['amount'],
                )
                for item in ingredients_data
            ]
        )

    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients', None)
        recipe = Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )
        self._save_ingredients(recipe, ingredients_data)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'image' in validated_data and instance.image:
            instance.image.delete(save=False)
        ingredients_data = validated_data.pop('recipe_ingredients', None)
        instance.ingredients.clear()
        instance = super().update(instance, validated_data)
        self._save_ingredients(instance, ingredients_data)
        return instance


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('recipe', 'user'),
                message='Рецепт уже добавлен в избранное',
            )
        ]

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe, context=self.context
        ).data
