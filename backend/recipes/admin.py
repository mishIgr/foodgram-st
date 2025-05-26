from django.contrib import admin

from .models import FavoriteRecipe, RecipeIngredient, Recipe


class IngredientRecipeInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "created_at", "favorites_count")
    readonly_fields = ("favorites_count",)
    search_fields = (
        "author__username",
        "name",
    )
    search_help_text = "Поиск по названию рецепта и автору"
    list_filter = ("created_at",)
    inlines = (IngredientRecipeInline,)

    @admin.display(description="Добавлений в избранное")
    def favorites_count(self, obj):
        return obj.favorites.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "ingredient",
        "amount",
    )
    search_fields = ("recipe__name", "ingredient__name")
    list_filter = ("amount",)


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "user",
    )
    search_fields = ("recipe__name", "user__username")
