from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Follow, MyUser
from api.models import Cart, FavoritedRecipe


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


class MyUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
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


admin.site.register(MyUser, MyUserAdmin)
