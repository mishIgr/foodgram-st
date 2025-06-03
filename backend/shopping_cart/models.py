from recipes.models import BaseUserRecipeRelation


class ShoppingCart(BaseUserRecipeRelation):

    class Meta(BaseUserRecipeRelation.Meta):
        default_related_name = 'shopping_cart'
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
