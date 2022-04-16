from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordChangeForm

from mytravelblog.common.helpers import BootstrapFormMixin, BIRTH_YEAR_RANGE
from mytravelblog.accounts.models import Profile
from mytravelblog.common.validators import validate_file_content_type

UserModel = get_user_model()


class UserLoginForm(AuthenticationForm, BootstrapFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your username',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    username = UsernameField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'placeholder': 'Enter username',
            }
        )
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'placeholder': 'Enter password',
            }),
    )

    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                'placeholder': 'Re-enter password',
            }),
        strip=False,
    )

    class Meta:
        model = UserModel

        fields = (
            'username',
            'password1',
            'password2',
        )


class EditPasswordForm(PasswordChangeForm, BootstrapFormMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    old_password = forms.CharField(
        label='Old Password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autofocus': True,
                'placeholder': 'Enter old password',
            },
        ),
    )

    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter new password',
            },
        ),
    )

    new_password2 = forms.CharField(
        label='New Password Confirmation',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter new password again',
            },
        ),
    )


class EditProfileForm(forms.ModelForm, BootstrapFormMixin):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['email'].initial = self.user.email
        self._init_bootstrap_form_controls()

    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter first name',
                'autofocus': True,
            },
        ),
        required=False,
    )

    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter last name',
            },
        ),
        required=False,
    )

    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter email',
            },
        ),
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        if self.cleaned_data['profile_picture']:
            validate_file_content_type('profile_picture', self.cleaned_data['profile_picture'].content_type)
        return cleaned_data

    class Meta:
        model = Profile

        fields = (
            'first_name',
            'last_name',
            'email',
            'profile_picture',
            'date_of_birth',
            'current_country',
        )

        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                years=BIRTH_YEAR_RANGE,
            ),
            'current_country': forms.TextInput(),
        }
