from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.query import Prefetch

from .models import FavoriteRecipe, Recipe, RecipeIngredient

User = get_user_model()


class IngredientRecipeInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created_at', 'favorites_count')
    readonly_fields = ('favorites_count',)
    search_fields = (
        'author__username',
        'name',
    )
    search_help_text = 'Поиск по названию рецепта и автору'
    inlines = (IngredientRecipeInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related(
            'author'
        ).prefetch_related(
            Prefetch('favorites', queryset=FavoriteRecipe.objects.only(
                'id', 'recipe')),
            Prefetch('recipe_ingredients',
                     queryset=RecipeIngredient.objects
                     .select_related('ingredient')),
        ).annotate(
            favorites_count=Count('favorites', distinct=True)
        )
        return queryset

    @admin.display(description='Добавлений в избранное')
    def favorites_count(self, obj):
        return obj.favorites_count


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = ('recipe__name', 'ingredient__name')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related(
            'recipe',
            'ingredient'
        )


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'user',
    )
    search_fields = ('recipe__name', 'user__username')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related(
            'recipe',
            'user'
        )
