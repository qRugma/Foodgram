import django_filters

from .models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        # queryset=Tag.objects.all(),
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='cart_method')
    is_favorited = django_filters.NumberFilter(
        method='favorited_method')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def cart_method(self, queryset, field_name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(
                who_cart__user = user)
        return queryset
    
    def favorited_method(self, queryset, field_name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(
                favorited__user = user)
        return queryset
