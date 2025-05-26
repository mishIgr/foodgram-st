from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe


User = get_user_model()


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        verbose_name='Рецепт', to=Recipe, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = 'shopping_cart'
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'

    def __str__(self):
        return str(self.recipe)
