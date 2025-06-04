from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    search_fields = ('user__username', 'author__username')
    search_help_text = 'Поиск по нику пользователя и автора'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related(
            'user',
            'author'
        )
