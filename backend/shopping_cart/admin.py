from django.contrib import admin

from .models import ShoppingCart


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "user",
    )
    search_fields = ("recipe__name", "user__username")
