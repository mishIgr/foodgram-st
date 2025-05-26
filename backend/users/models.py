from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=254,
        help_text='Адрес электронной почты',
    )
    username = models.CharField(
        verbose_name='Ник пользоваля',
        unique=True,
        max_length=150,
        validators=[UnicodeUsernameValidator()],
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользоваля',
        max_length=150,
    )
    first_name = models.CharField(
        verbose_name='Имя пользоваля',
        max_length=150,
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to=getattr(settings, 'UPLOAD_AVATAR', 'users/images/'),
        null=True,
        blank=True,
        default=None,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
