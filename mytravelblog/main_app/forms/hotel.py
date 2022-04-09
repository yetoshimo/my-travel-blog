from django import forms

from mytravelblog.accounts.helpers import BootstrapFormMixin
from mytravelblog.main_app.models import VisitedHotel


class HotelRegistrationForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, located_city, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()
        self.fields['located_city'].queryset = located_city

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
    def __init__(self, located_city, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.fields['located_city'].queryset = located_city

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
