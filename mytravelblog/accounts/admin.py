from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mytravelblog.accounts.models import *

UserModel = get_user_model()


class ProfileInlineAdmin(admin.StackedInline):
    model = Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_country',)
    list_filter = ('user', 'current_country',)
    ordering = ('user',)


admin.site.unregister(UserModel)


@admin.register(UserModel)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff')
    inlines = (ProfileInlineAdmin,)
