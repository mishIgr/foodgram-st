from django.contrib import admin

from .models import ShortUrl


@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    list_display = (
        "origin_url",
        "short_url",
    )
    search_fields = ("origin_url", "short_url")
