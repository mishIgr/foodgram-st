from django.http import HttpResponse
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ShoppingCartSerializer
from .models import Recipe, ShoppingCart
from recipes.models import RecipeIngredient


class ShoppingCartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        serializer = ShoppingCartSerializer(
            data={'user': request.user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        get_object_or_404(Recipe, pk=recipe_id)
        cart_items = ShoppingCart.objects.filter(
            user=request.user,
            recipe_id=recipe_id
        )

        if not cart_items.exists():
            return Response(
                {'detail': 'Рецепт не найден в вашей корзине'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # user_cart = ShoppingCart.objects.filter(user=request.user)

        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            total_amount=Sum('amount')
        ).order_by('ingredient__name')

        txt_content = "Список покупок:\n\n"
        for idx, ingredient in enumerate(ingredients, start=1):
            txt_content += (
                f"{idx}. {ingredient['ingredient__name']} - "
                f"{ingredient['total_amount']} "
                f"{ingredient['ingredient__measurement_unit']}\n"
            )

        txt_content += "\nFoodgram - Ваш кулинарный помощник!"

        response = HttpResponse(txt_content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response
