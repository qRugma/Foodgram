from django.contrib import admin

from .models import Follow, MyUser


class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = 'user'
    extra = 0


class MyUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    model = MyUser
    inlines = (FollowInline,)


admin.site.register(MyUser, MyUserAdmin)
