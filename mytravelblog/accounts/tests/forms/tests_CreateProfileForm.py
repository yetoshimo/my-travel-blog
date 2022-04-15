from django import test as django_tests
from django.contrib.auth import get_user_model

from mytravelblog.accounts.forms import UserLoginForm, CreateProfileForm

UserModel = get_user_model()


class CreateProfileFormTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'

    def tests_create_profile_form_populates_with_form_control_attribute(self):
        data = {
            'username': self.username,
            'password1': self.password1,
            'password2': self.password1,
        }
        create_profile_form = CreateProfileForm(data=data)
        self.assertTrue(create_profile_form.is_valid())
        self.assertEqual('form-control', create_profile_form.fields['username'].widget.attrs['class'])
