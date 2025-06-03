from django.db import models

from . import constants


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=constants.NAME_MAX_LENGTH
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=constants.MEASUREMENT_UNIT_MAX_LENGTH
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='name_measurement_unit',
            )
        ]

    def __str__(self):
        return self.name
