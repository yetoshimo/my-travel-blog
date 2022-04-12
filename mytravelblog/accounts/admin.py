from django.contrib import admin
from django.db.models import signals
from django.dispatch import receiver

from mytravelblog.accounts.forms import CreateProfileForm, EditProfileForm
from mytravelblog.accounts.models import *


@receiver(signals.post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:
        instance.user.delete()


@admin.register(MyTravelBlogUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'current_country',)
    list_filter = ('current_country',)
    form = CreateProfileForm
    ordering = ('id',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=None, change=False, **kwargs)
        if change:
            p = Profile.objects.get(user=obj)
            form.base_fields['first_name'].initial = p.first_name
            form.base_fields['last_name'].initial = p.last_name
            form.base_fields['profile_picture'].initial = p.profile_picture
            form.base_fields['password1'].required = False
            form.base_fields['password2'].required = False
            return form
        return form

    def save_model(self, request, obj, form, change):
        if not change:
            super().save_model(request, obj, form, change)
            Profile.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                profile_picture=form.cleaned_data['profile_picture'],
                user=obj,
            )
        else:
            # TODO - CORRECT THIS
            __initial_password = MyTravelBlogUser.objects.get(email=obj.email).password
            if form.cleaned_data['password1'] != '' or form.cleaned_data['password2'] != '':
                super().save_model(request, obj, form, change)
            else:
                super().save_model(request, obj, form, change)
                user = MyTravelBlogUser.objects.get(email=obj.email)
                user.password = __initial_password
                user.save()
            p = Profile.objects.get(user=obj)
            p.first_name = form.cleaned_data['first_name']
            p.last_name = form.cleaned_data['last_name']
            p.profile_picture = form.cleaned_data['profile_picture']
            p.save()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    readonly_fields = ('user',)
    ordering = ('user',)

    def has_add_permission(self, request, obj=None):
        return False
