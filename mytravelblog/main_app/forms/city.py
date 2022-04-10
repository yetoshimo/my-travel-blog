from django import forms

from mytravelblog.accounts.helpers import BootstrapFormMixin
from mytravelblog.main_app.models import VisitedCity


class CityRegistrationForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['country_name'] = self.cleaned_data['country_name'].title()
        cleaned_data['city_name'] = self.cleaned_data['city_name'].title()
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['country_name'] = self.cleaned_data['country_name'].title()
        self.cleaned_data['city_name'] = self.cleaned_data['city_name'].title()
        return cleaned_data

    class Meta:
        model = VisitedCity

        fields = (
            'city_name',
            'country_name',
        )


class CityDeleteForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = VisitedCity

        fields = (
        )
