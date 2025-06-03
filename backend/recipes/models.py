from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from ingredients.models import Ingredient

from . import constants

User = get_user_model()


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Наименование рецепта',
        max_length=constants.RECIPE_NAME_MAX_LENGTH,
        db_index=True,
    )
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                limit_value=constants.MIN_COOKING_TIME,
                message=constants.COOKING_TIME_MIN_MESSAGE
            ),
            MaxValueValidator(
                limit_value=constants.MAX_COOKING_TIME,
                message=constants.COOKING_TIME_MAX_MESSAGE,
            ),
        ],
        help_text=constants.COOKING_TIME_HELP_TEXT,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=settings.UPLOAD_RECIPES
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
    )
    author = models.ForeignKey(
        verbose_name='Автор',
        to=User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено', auto_now_add=True
    )

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        verbose_name='Рецепт', to=Recipe, on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        verbose_name='Ингредиент', to=Ingredient, on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                limit_value=constants.MIN_INGREDIENT_AMOUNT,
                message=constants.INGREDIENT_MIN_MESSAGE,
            ),
            MaxValueValidator(
                limit_value=constants.MAX_INGREDIENT_AMOUNT,
                message=constants.INGREDIENT_MAX_MESSAGE,
            ),
        ],
    )

    class Meta:
        default_related_name = 'recipe_ingredients'
        verbose_name = 'Ингредиент в составе рецепта'
        verbose_name_plural = 'Ингредиенты в составе рецептов'

    def __str__(self):
        return f'{self.ingredient}'


class BaseUserRecipeRelation(models.Model):
    recipe = models.ForeignKey(
        'recipes.Recipe',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
        unique_together = ('user', 'recipe')

    def __str__(self):
        return self.recipe.name


class FavoriteRecipe(BaseUserRecipeRelation):

    class Meta(BaseUserRecipeRelation.Meta):
        default_related_name = 'favorites'
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
