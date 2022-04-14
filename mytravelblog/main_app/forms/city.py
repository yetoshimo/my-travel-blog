from django import forms
from django.core.exceptions import ValidationError

from mytravelblog.accounts.helpers import BootstrapFormMixin
from mytravelblog.main_app.models import VisitedCity


def _validate_city_name(user, city_name, country_name):
    _city_name = city_name.title()
    _country_name = country_name.title()
    if VisitedCity.objects.filter(user=user,
                                  city_name=_city_name,
                                  country_name=_country_name).exists():
        raise ValidationError(f'{_city_name} '
                              f'in {_country_name} already exists!')
    return _city_name, _country_name


class CityRegistrationForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['city_name'], \
        self.cleaned_data['country_name'] = \
            _validate_city_name(self.user, self.cleaned_data['city_name'], self.cleaned_data['country_name'])
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
        self.cleaned_data['city_name'], \
        self.cleaned_data['country_name'] = \
            _validate_city_name(self.user, self.cleaned_data['city_name'], self.cleaned_data['country_name'])
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
