from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    search_fields = ('username', 'email', 'avatar')
    search_help_text = 'Поиск по нику или электронной почте'
