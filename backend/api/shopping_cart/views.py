from io import StringIO

from django.db.models import Sum
from django.db.models.functions import Lower
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.base.recipe_actions import BaseRecipeActionView
from recipes.models import RecipeIngredient
from shopping_cart.models import ShoppingCart

from .serializers import ShoppingCartSerializer


class ShoppingCartAPIView(BaseRecipeActionView):
    model = ShoppingCart
    serializer_class = ShoppingCartSerializer
    not_found_message = 'Рецепт не найден в вашей корзине'


class DownloadShoppingCartView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        ingredients = self._get_shopping_cart_ingredients(request.user)
        txt_content = self._generate_shopping_list_content(ingredients)
        return self._create_file_response(txt_content)

    def _get_shopping_cart_ingredients(self, user):
        return RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=user
        ).values(
            'ingredient__measurement_unit',
            lower_name=Lower('ingredient__name')
        ).annotate(
            total_amount=Sum('amount')
        ).order_by('lower_name')

    def _generate_shopping_list_content(self, ingredients):
        buffer = StringIO()
        buffer.write('Список покупок:\n\n')

        for idx, ingredient in enumerate(ingredients, start=1):
            buffer.write(
                f'{idx}. {ingredient["lower_name"]} - '
                f'{ingredient["total_amount"]} '
                f'{ingredient["ingredient__measurement_unit"]}\n'
            )

        buffer.write('\nFoodgram - Ваш кулинарный помощник!')
        return buffer.getvalue()

    def _create_file_response(self, content, filename='shopping_cart.txt'):
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
