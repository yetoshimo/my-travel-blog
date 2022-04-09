from django.contrib import admin

from mytravelblog.accounts.models import *


@admin.register(MyTravelBlogUser)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'current_country',)
    list_filter = ('current_country',)
    readonly_fields = ('email',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    readonly_fields = ('user',)
