from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from ingredients.models import Ingredient


User = get_user_model()


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Наименование рецепта',
        max_length=256,
        db_index=True,
    )
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                limit_value=1, message='Значение не может быть меньше 1!'
            ),
            MaxValueValidator(
                limit_value=43_200,
                message=(
                    'Максимальное значение не может',
                    'превышать 30 дней (43200 минут)!',
                ),
            ),
        ],
        help_text='Введите значение больше или равное 1',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=getattr(settings, 'UPLOAD_RECIPES', 'recipes/images/'),
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
                limit_value=1,
                message='Количество ингредиентов не может быть меньше 1!',
            ),
            MaxValueValidator(
                limit_value=1000,
                message='Количество ингредиентов не может быть больше 1000!',
            ),
        ],
    )

    class Meta:
        default_related_name = 'recipe_ingredients'
        verbose_name = 'Ингредиент в составе рецепта'
        verbose_name_plural = 'Ингредиенты в составе рецептов'

    def __str__(self):
        return f'{self.ingredient}'


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(
        verbose_name='Рецепт', to=Recipe, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = 'favorites'
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return str(self.recipe)
