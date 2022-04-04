from django_filters import CharFilter, FilterSet
from django_filters.filters import BooleanFilter

from .models import Ingredients, Recipe


class RecipeFilter(FilterSet):
    tags = CharFilter(field_name='tags__slug', method='filter_tags')
    is_favorite = BooleanFilter(method='filter_is_favorite')
    is_in_shopping_cart = BooleanFilter(method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('is_favorite', 'is_in_shopping_cart', 'author', 'tags')

    def filter_tags(self, queryset, slug, tags):
        tags = self.request.query_params.getlist('tags')
        return queryset.filter(
            tags__slug__in=tags
        ).distinct()

    def filter_is_favorite(self, queryset, is_favorite, slug):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        is_favorite = self.request.query_params.get('is_favorite')
        if is_favorite:
            return queryset.filter(
                is_favorited__user=self.request.user
            ).distinct()
        return queryset

    def filter_is_in_shopping_cart(self, queryset, is_in_shopping_cart, slug):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart',
        )
        if is_in_shopping_cart:
            return queryset.filter(
                is_in_shopping_cart__user=self.request.user
            ).distinct()
        return queryset


class IngredientNameFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredients
        fields = ('name',)
