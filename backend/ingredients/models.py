from django.db import models


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=128
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='name_measurement_unit',
            )
        ]

    def __str__(self):
        return f'{self.name}'
