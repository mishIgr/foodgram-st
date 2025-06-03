from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    author = models.ForeignKey(
        verbose_name='Отслеживаемый автор',
        to=User,
        on_delete=models.CASCADE,
        related_name='subscribers',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'), name='unique_following'
            ),
        )

    def __str__(self):
        return self.user.username

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Нельзя подписаться на самого себя.')
        return super().clean()
