from django import test as django_tests
from django.contrib.auth import get_user_model

from mytravelblog.accounts.forms import UserLoginForm

UserModel = get_user_model()


class UserLoginFormTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'

        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

    def test_form_populates_with_form_control_attribute(self):
        data = {
            'username': self.username,
            'password': self.password1,
        }
        login_form = UserLoginForm(data=data)
        self.assertTrue(login_form.is_valid())
        self.assertEqual('form-control', login_form.fields['username'].widget.attrs['class'])
