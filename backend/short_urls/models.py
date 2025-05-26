import random

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class ShortUrl(models.Model):
    origin_url = models.URLField(
        verbose_name='Исходная ссылка', primary_key=True
    )
    short_url = models.SlugField(
        verbose_name='Короткая ссылка',
        max_length=1000,
        unique=True,
        db_index=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Короткая ссылка'
        verbose_name_plural = 'Короткие ссылки'

    def generate_short_url(self):
        alphabet_token = settings.ALPHABET_TOKEN_SHORT_URL
        len_token = settings.LENGTH_TOKEN_SHORT_URL

        if ShortUrl.objects.count() >= len(alphabet_token) ** len_token:
            raise ValidationError(
                'No more short URLs available. Database limit reached.'
            )

        while True:
            token = ''.join(random.choices(alphabet_token, k=len_token))
            short_url = f'/s/{token}/'
            if not ShortUrl.objects.filter(short_url=short_url).exists():
                self.short_url = short_url
                break

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.generate_short_url()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.short_url
