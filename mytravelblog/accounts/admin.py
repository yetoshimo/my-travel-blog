from django.contrib import admin
from django.db.models import signals
from django.dispatch import receiver

from mytravelblog.accounts.forms import CreateProfileForm
from mytravelblog.accounts.models import *


class ProfileInlineAdmin(admin.StackedInline):
    model = Profile


@receiver(signals.post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:
        instance.user.delete()


@admin.register(MyTravelBlogUser)
class UserAdmin(admin.ModelAdmin):
    model = Profile
    form = CreateProfileForm
    list_display = ('email', 'current_country',)
    list_filter = ('current_country',)
    exclude = (
        'password',
        'last_login',
    )

    fields = (
        'email',
        'current_country',
        'is_staff',
        'is_superuser',
        'groups',
        'user_permissions',
        'first_name',
        'last_name',
        'profile_picture',
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    readonly_fields = ('user',)

    def has_add_permission(self, request, obj=None):
        return False
