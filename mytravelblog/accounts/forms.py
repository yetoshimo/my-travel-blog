from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator

from mytravelblog.accounts.helpers import BootstrapFormMixin, BIRTH_YEAR_RANGE
from mytravelblog.accounts.models import Profile, MyTravelBlogUser
from mytravelblog.accounts.validators import *

UserModel = get_user_model()


class UserLoginForm(AuthenticationForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    username = UsernameField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email',
                'autofocus': True,
            },
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
            },
        ),
    )


class CreateProfileForm(UserCreationForm, BootstrapFormMixin):
    FIRST_NAME_MAX_LENGTH = 32
    FIRST_NAME_MIN_LENGTH = 2

    LAST_NAME_MAX_LENGTH = 32
    LAST_NAME_MIN_LENGTH = 2

    URL_FIELD_MAX_LENGTH = 200

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.fields['profile_picture'].required = False

    email = forms.EmailField(
        label='Email:',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email address',
                'autofocus': True,
            },
        ),
    )

    password1 = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password'
            },
        ),
    )

    password2 = forms.CharField(
        label='Password Confirmation:',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter the same password as before, for verification.'
            },
        ),
    )

    current_country = forms.CharField(
        label='Current Country:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter current country'
            }
        )
    )

    first_name = forms.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        label='First Name:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter first name',
            },
        ),
    )

    last_name = forms.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        label='Last Name:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter last name',
            },
        ),
    )

    profile_picture = forms.URLField(
        label='Profile Picture URL:',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter profile picture URL',
            },
        ),
        validators=(
            MaxLengthValidator(URL_FIELD_MAX_LENGTH),
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        cleaned_data['current_country'] = self.cleaned_data.get('current_country').title()
        validate_first_name(first_name)
        validate_first_name_length(first_name)
        validate_last_name(last_name)
        validate_last_name_length(last_name)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            profile_picture=self.cleaned_data['profile_picture'],
            user=user,
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = UserModel

        fields = (
            'email',
            'first_name',
            'last_name',
            'current_country',
            'profile_picture',
            'password1',
            'password2',
        )


class EditPasswordForm(PasswordChangeForm, BootstrapFormMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    old_password = forms.CharField(
        label='Old Password:',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autofocus': True,
                'placeholder': 'Enter old password',
            },
        ),
    )

    new_password1 = forms.CharField(
        label='New Password:',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter new password',
            },
        ),
    )

    new_password2 = forms.CharField(
        label='New Password Confirmation:',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter new password again',
            },
        ),
    )


class EditProfileForm(forms.ModelForm, BootstrapFormMixin):
    EMAIL_MAX_LENGTH = 254
    COUNTRIES_MAX_LENGTH = 50
    COUNTRIES_MIN_LENGTH = 4

    def __init__(self, email, current_country, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.initial['email'] = email
        self.initial['current_country'] = current_country

    email = forms.EmailField(
        label='Email:',
        validators=(
            MaxLengthValidator(EMAIL_MAX_LENGTH),
        )
    )

    current_country = forms.CharField(
        label='Current Country:',
        validators=(
            MaxLengthValidator(COUNTRIES_MAX_LENGTH),
            MinLengthValidator(COUNTRIES_MIN_LENGTH),
        )
    )

    def clean(self):
        __initial_email = self.initial['email']
        cleaned_data = super().clean()
        email = self.cleaned_data['email']
        if __initial_email != email and MyTravelBlogUser.objects.filter(email=email).exists():
            raise ValidationError(f'User with this Email already exists.')
        return cleaned_data

    class Meta:
        model = Profile

        fields = (
            'first_name',
            'last_name',
            'profile_picture',
            'date_of_birth',
            'email',
            'current_country',
        )

        labels = {
            'profile_picture': 'Profile Picture:',
        }

        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                years=BIRTH_YEAR_RANGE,
            ),
            'email': forms.EmailInput(),
            'current_country': forms.TextInput(),
            'profile_picture': forms.URLInput(
                attrs={
                    'placeholder': 'Enter profile picture URL',
                },
            ),
        }
