from django.db.models import Exists, OuterRef
from django.db.models.query import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.base.permissions import IsAuthorOrReadOnlyPermission
from api.base.recipe_actions import BaseRecipeActionView
from recipes.models import FavoriteRecipe, Recipe, RecipeIngredient

from .filters import ProductFilter
from .serializers import FavoriteRecipeSerializer, RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author',)
    filterset_class = ProductFilter

    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.select_related(
            'author'
        ).prefetch_related(
            Prefetch(
                'recipe_ingredients',
                queryset=RecipeIngredient.objects.select_related('ingredient')
            )
        )

        if user.is_authenticated:
            queryset = queryset.annotate(
                is_favorited=Exists(
                    user.favorites.filter(recipe_id=OuterRef('pk'))
                ),
                is_in_shopping_cart=Exists(
                    user.shopping_cart.filter(recipe_id=OuterRef('pk'))
                )
            )

        return queryset

    def perform_destroy(self, instance):
        if instance.image:
            instance.image.delete(save=False)
        instance.delete()


class FavoriteAPIView(BaseRecipeActionView):
    model = FavoriteRecipe
    serializer_class = FavoriteRecipeSerializer
    not_found_message = 'Рецепт не был добавлен в избранное'
