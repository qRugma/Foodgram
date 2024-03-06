import django_filters

from .models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter(
        field_name='author', lookup_expr='exact')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
