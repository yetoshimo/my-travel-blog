from django import forms

from mytravelblog.accounts.helpers import BootstrapFormMixin
from mytravelblog.main_app.models import TravelEntry


class TravelEntryRegistrationForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, visited_city, visited_hotel, travel_picture, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()
        self.fields['travel_picture'].queryset = travel_picture
        self.fields['visited_hotel'].queryset = visited_hotel
        self.fields['visited_city'].queryset = visited_city

    def save(self, commit=True):
        travel_entry = super().save(commit=False)
        travel_entry.user = self.user
        if commit:
            travel_entry.save()

        return travel_entry

    class Meta:
        model = TravelEntry

        fields = (
            'title',
            'description',
            'visited_city',
            'visited_hotel',
            'travel_picture',
        )


class TravelEntryEditForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, visited_city, visited_hotel, travel_picture, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()
        self.fields['travel_picture'].queryset = travel_picture
        self.fields['visited_hotel'].queryset = visited_hotel
        self.fields['visited_city'].queryset = visited_city

    class Meta:
        model = TravelEntry

        fields = (
            'title',
            'description',
            'visited_city',
            'visited_hotel',
            'travel_picture',
        )


class TravelEntryDeleteForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = TravelEntry

        fields = (
        )
