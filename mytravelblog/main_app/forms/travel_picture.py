from django import forms

from mytravelblog.accounts.helpers import BootstrapFormMixin
from mytravelblog.main_app.models import TravelPicture


class TravelPictureRegistrationForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, located_city, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()
        self.fields['located_city'].queryset = located_city

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
            'title',
            'travel_picture',
            'located_city',
        )

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'autofocus': True,
                    'placeholder': 'Enter title',
                },
            ),
        }


class TravelPictureEditForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, located_city, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.fields['located_city'].queryset = located_city

    class Meta:
        model = TravelPicture

        fields = (
            'title',
            'travel_picture',
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
