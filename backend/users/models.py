from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from . import constants


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=constants.EMAIL_MAX_LENGTH,
        help_text='Адрес электронной почты',
    )
    username = models.CharField(
        verbose_name='Ник пользователя',
        unique=True,
        max_length=constants.USERNAME_MAX_LENGTH,
        validators=(UnicodeUsernameValidator(),),
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=constants.NAME_MAX_LENGTH,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=constants.NAME_MAX_LENGTH,
    )
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to=settings.UPLOAD_AVATAR,
        default='',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
