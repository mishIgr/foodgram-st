from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    search_fields = ('username', 'email', 'avatar')
    search_help_text = 'Поиск по нику или электронной почте'
