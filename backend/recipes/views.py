from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .filters import ProductFilter
from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import RecipeSerializer, FavoriteRecipeSerializer
from .models import Recipe, FavoriteRecipe


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("author",)
    filterset_class = ProductFilter


class FavoriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        serializer = FavoriteRecipeSerializer(
            data={'user': request.user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        get_object_or_404(Recipe, pk=recipe_id)
        favorite_recipe = FavoriteRecipe.objects.filter(
            user=request.user,
            recipe_id=recipe_id
        )

        if not favorite_recipe.exists():
            return Response(
                {'detail': 'Рецепт не был добавлен в избранное'},
                status=status.HTTP_400_BAD_REQUEST
            )

        favorite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
