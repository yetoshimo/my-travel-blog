from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.accounts.models import Profile

UserModel = get_user_model()


class UserRegisterViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword1'

    def test_user_registration_page_url(self):
        response = self.client.get('/accounts/profile/create/')
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, template_name='accounts/profile/profile_create.html')

    def test_user_registration_page_view_name(self):
        response = self.client.get(reverse('profile create'))
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, template_name='accounts/profile/profile_create.html')

    def test_user_registration_form_valid_data(self):
        response = self.client.post(
            reverse('profile create'),
            data={
                'username': self.username,
                'password1': self.password1,
                'password2': self.password2,
            }
        )
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertRedirects(response, reverse('show dashboard'))
        self.assertIn('_auth_user_id', self.client.session)
        users = UserModel.objects.all()
        self.assertEqual(1, users.count())
        profiles = Profile.objects.all()
        self.assertEqual(1, profiles.count())
        self.assertEqual(users[0], profiles[0].user)

    def test_user_registration_form_invalid_username(self):
        self.client.post(
            reverse('profile create'),
            data={
                'username': self.username,
                'password1': self.password1,
                'password2': self.password2,
            }
        )
        response_invalid_data = self.client.post(
            reverse('profile create'),
            data={
                'username': self.username,
                'password1': self.password1,
                'password2': self.password2,
            }
        )
        self.assertEqual(HTTPStatus.OK, response_invalid_data.status_code)
        users = UserModel.objects.all()
        self.assertEqual(1, users.count())
