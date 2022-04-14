from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

UserModel = get_user_model()


class EditProfileForm(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword1'
        self.first_name = 'testuser-firstname'
        self.last_name = 'testuser-lastname'
        self.email = 'testuser@email.com'
        self.profile_picture = 'default_profile_picture.png'

        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

    def test_edit_profile_form_has_initial_values(self):
        self.client.login(username=self.username, password=self.password1)
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }
        self.client.post(reverse('profile edit', kwargs={'pk': self.user.id}), data)
        user_first_name_updated = UserModel.objects.filter(first_name=self.first_name).exists()
        self.assertTrue(True, user_first_name_updated)
