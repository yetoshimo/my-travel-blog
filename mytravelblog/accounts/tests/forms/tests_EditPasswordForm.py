from django import test as django_tests
from django.contrib.auth import get_user_model

from mytravelblog.accounts.forms import UserLoginForm, EditPasswordForm

UserModel = get_user_model()


class EditPasswordFromTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'

        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

    def test_form_populates_with_form_control_attribute(self):
        data = {
            'old_password': self.password1,
            'new_password1': self.password1,
            'new_password2': self.password1,
        }
        change_password_form = EditPasswordForm(data=data, user=self.user)
        self.assertTrue(change_password_form.is_valid())
        self.assertEqual('form-control', change_password_form.fields['old_password'].widget.attrs['class'])
