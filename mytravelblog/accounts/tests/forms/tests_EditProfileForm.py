from django import test as django_tests
from django.contrib.auth import get_user_model

from mytravelblog.accounts.forms import EditProfileForm

UserModel = get_user_model()


class EditProfileFormTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword1'
        self.first_name = 'testuser-firstname'
        self.last_name = 'testuser-lastname'
        self.email = 'testuser@email.com'
        self.first_name_update = 'testuser-firstname-update'
        self.profile_picture = 'default_profile_picture.png'

        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
        )

    def test_edit_profile_form_has_initial_values(self):
        data = {
            'first_name': self.first_name_update,
        }
        edit_profile_form = EditProfileForm(data=data, user=self.user)
        self.assertTrue(edit_profile_form.is_valid())
        self.assertEqual('form-control', edit_profile_form.fields['first_name'].widget.attrs['class'])
        self.assertEqual(self.first_name, edit_profile_form.fields['first_name'].initial)
        self.assertEqual(self.last_name, edit_profile_form.fields['last_name'].initial)
        self.assertEqual(self.email, edit_profile_form.fields['email'].initial)
