from django import forms
from django.core.exceptions import ValidationError

from mytravelblog.accounts.helpers import BootstrapFormMixin
from mytravelblog.main_app.models import VisitedHotel


def _validate_hotel_name(user, hotel_name, located_city):
    _hotel_name = hotel_name
    _located_city = located_city
    if VisitedHotel.objects.filter(user=user,
                                   hotel_name=_hotel_name,
                                   located_city=_located_city).exists():
        raise ValidationError(f'{_hotel_name} in {_located_city} already exists!')


class HotelRegistrationForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, located_city, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()
        self.fields['located_city'].queryset = located_city

    def clean(self):
        cleaned_data = super().clean()
        _validate_hotel_name(self.user, self.cleaned_data['hotel_name'], self.cleaned_data['located_city'])
        return cleaned_data

    def save(self, commit=True):
        visited_hotel = super().save(commit=False)
        visited_hotel.user = self.user
        if commit:
            visited_hotel.save()

        return visited_hotel

    class Meta:
        model = VisitedHotel

        fields = (
            'hotel_name',
            'number_of_stars',
            'located_city',
        )

        widgets = {
            'hotel_name': forms.TextInput(
                attrs={
                    'autofocus': True,
                    'placeholder': 'Enter hotel name',
                },
            ),
        }


class HotelEditForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, located_city, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()
        self.fields['located_city'].queryset = located_city

    def clean(self):
        cleaned_data = super().clean()
        _validate_hotel_name(self.user, self.cleaned_data['hotel_name'], self.cleaned_data['located_city'])
        return cleaned_data

    class Meta:
        model = VisitedHotel

        fields = (
            'hotel_name',
            'number_of_stars',
            'located_city',
        )


class HotelDeleteForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = VisitedHotel

        fields = (
        )
