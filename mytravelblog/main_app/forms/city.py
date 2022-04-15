from django import forms
from django.core.exceptions import ValidationError

from mytravelblog.common.helpers import BootstrapFormMixin
from mytravelblog.main_app.models import VisitedCity


def _validate_city_name(user, city_name, country_name):
    _city_name = city_name.title()
    _country_name = country_name.title()
    if VisitedCity.objects.filter(user=user,
                                  city_name=_city_name,
                                  country_name=_country_name).exists():
        raise ValidationError({
            'city_name': f'{_city_name} in {_country_name} already exists!'
        })


class CityRegistrationForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def clean(self):
        cleaned_data = super().clean()
        _validate_city_name(self.user, self.cleaned_data['city_name'], self.cleaned_data['country_name'])
        cleaned_data['city_name'] = cleaned_data['city_name'].title()
        cleaned_data['country_name'] = cleaned_data['country_name'].title()
        return cleaned_data

    def save(self, commit=True):
        visited_city = super().save(commit=False)
        visited_city.user = self.user
        if commit:
            visited_city.save()

        return visited_city

    class Meta:
        model = VisitedCity

        fields = (
            'city_name',
            'country_name',
        )

        widgets = {
            'city_name': forms.TextInput(
                attrs={
                    'autofocus': True,
                    'placeholder': 'Enter city name',
                },
            ),
            'country_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter country name',
                },
            ),
        }


class CityEditForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def clean(self):
        cleaned_data = super().clean()
        if self.changed_data:
            _validate_city_name(self.user, self.cleaned_data['city_name'], self.cleaned_data['country_name'])
        cleaned_data['city_name'] = cleaned_data['city_name'].title()
        cleaned_data['country_name'] = cleaned_data['country_name'].title()
        return cleaned_data

    class Meta:
        model = VisitedCity

        fields = (
            'city_name',
            'country_name',
        )

        widgets = {
            'city_name': forms.TextInput(
                attrs={
                    'autofocus': True,
                },
            ),
        }


class CityDeleteForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = VisitedCity

        fields = (
        )
