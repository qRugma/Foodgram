from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    search_fields = ('name',)
    list_display = (
        'name',
        'measurement_unit'
    )


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


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


class TagInline(admin.TabularInline):
    model = RecipeTag
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    model = Recipe
    inlines = (RecipeIngredientInline, TagInline)
    search_fields = (
        'name', 'author__email', 'tags__slug',
        'tags__name',)
    list_filter = ('tags',)
    readonly_fields = ('favorited',)

    def favorited(self, obj):
        return obj.favorited.count()
    favorited.short_description = 'Лайков'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
