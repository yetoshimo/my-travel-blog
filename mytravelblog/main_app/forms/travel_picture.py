from django import forms
from django.core.exceptions import ValidationError

from mytravelblog.common.helpers import BootstrapFormMixin
from mytravelblog.main_app.models import TravelPicture


def _validate_travel_picture_name(user, title, located_city):
    _title = title
    _located_city = located_city
    if TravelPicture.objects.filter(user=user,
                                    title=_title,
                                    located_city=_located_city,
                                    ).exists():
        raise ValidationError({
            'title': f'Picture with title "{_title}" in {_located_city} already exists!'
        })


class TravelPictureRegistrationForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, located_city, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()
        self.fields['located_city'].queryset = located_city

    def clean(self):
        cleaned_data = super().clean()
        _validate_travel_picture_name(self.user, self.cleaned_data['title'], self.cleaned_data['located_city'])
        return cleaned_data

    def save(self, commit=True):
        travel_picture = super().save(commit=False)
        travel_picture.user = self.user
        travel_picture.located_city = self.cleaned_data['located_city']

        if commit:
            travel_picture.save()

        return travel_picture

    class Meta:
        model = TravelPicture

        fields = (
            'travel_picture',
            'title',
            'located_city',
        )

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'autofocus': True,
                    'placeholder': 'Enter unique title',
                },
            ),
        }


class TravelPictureEditForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, located_city, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()
        self.fields['located_city'].queryset = located_city

    def clean(self):
        cleaned_data = super().clean()
        if 'title' in self.changed_data or 'located_city' in self.changed_data:
            _validate_travel_picture_name(self.user, self.cleaned_data['title'], self.cleaned_data['located_city'])
        return cleaned_data

    class Meta:
        model = TravelPicture

        fields = (
            'travel_picture',
            'title',
            'located_city',
        )


class TravelPictureDeleteForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = TravelPicture

        fields = (
        )
