from django_filters.rest_framework import BooleanFilter, FilterSet

from recipes.models import Recipe


class ProductFilter(FilterSet):
    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        return self.filter_by_user_field(queryset, 'favorites', value)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return self.filter_by_user_field(queryset, 'shopping_cart', value)

    def filter_by_user_field(self, queryset, field_name, value):
        current_user = self.request.user
        if value and not current_user.is_anonymous:
            return queryset.filter(**{f'{field_name}__user': current_user})
        return queryset
