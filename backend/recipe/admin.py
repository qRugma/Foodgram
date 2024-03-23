from django.contrib import admin

from .models import (
    Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag,
    FavoritedRecipe
)
from foodgram.settings import ITEMS_ON_ADMIN_PAGE


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    search_fields = ('name',)
    list_display = (
        'name',
        'measurement_unit'
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = (
        'slug',
        'name',
        'color',
    )
    list_editable = (
        'name',
        'color',
    )
    search_fields = ('name', 'slug',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    model = RecipeIngredient
    list_display = (
        'recipe',
        'ingredient',
    )


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    model = RecipeTag
    list_display = (
        'recipe',
        'tag',
    )


@admin.register(FavoritedRecipe)
class FavoritedRecipeAdmin(admin.ModelAdmin):
    model = FavoritedRecipe
    list_display = (
        'recipe',
        'user',
    )


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    min_num = 1
# но можно удалить ингредиенты до нуля...


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 0
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'tags_display',
        'ingredients_display',
    )
    model = Recipe
    inlines = (RecipeIngredientInline, RecipeTagInline)
    search_fields = (
        'name', 'author__email', 'tags__slug',
        'tags__name',)
    list_filter = ('tags',)
    readonly_fields = ('favorited',)

    @admin.display(description='Теги')
    def tags_display(self, obj):
        return ", ".join([
            tag.name for tag in obj.tags.all()[:ITEMS_ON_ADMIN_PAGE]
        ])

    @admin.display(description='Ингредиенты')
    def ingredients_display(self, obj):
        return ", ".join([
            ingredient.name for ingredient
            in obj.ingredients.all()[:ITEMS_ON_ADMIN_PAGE]
        ])

    @admin.display(description='Количество лайков')
    def favorited(self, obj):
        return obj.favorited.count()
