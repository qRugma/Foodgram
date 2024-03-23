from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import TokenProxy

from .models import Follow, MyUser
from recipe.models import Cart, FavoritedRecipe


class StandartInline(admin.TabularInline):
    model = Follow
    fk_name = 'user'
    extra = 0


class FollowInline(StandartInline):
    model = Follow


class FavoritedRecipeInline(StandartInline):
    model = FavoritedRecipe


class CartInline(StandartInline):
    model = Cart


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'recipes_count',
        'followers_count',
    )
    search_fields = (
        'email',
        'username',
    )
    inlines = (
        FollowInline,
        FavoritedRecipeInline,
        CartInline,
    )

    @admin.display(description='Рецептов')
    def recipes_count(self, obj):
        return obj.recipes.count()

    @admin.display(description='Подписчиков')
    def followers_count(self, obj):
        return obj.followers.count()


admin.site.register(Follow)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
