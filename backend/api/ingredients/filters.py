from django_filters.rest_framework import CharFilter, FilterSet

from ingredients.models import Ingredient


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
