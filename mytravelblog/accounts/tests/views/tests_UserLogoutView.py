from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

UserModel = get_user_model()


class UserLogoutViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

    def test_user_logout_page_url(self):
        self.client.login(username=self.username, password=self.password1)
        self.client.get(reverse('logout user confirmation'))

        response = self.client.post('/accounts/logout/signout/')
        self.assertEqual(HTTPStatus.FOUND, response.status_code)

    def test_user_logout_page_view_name(self):
        self.client.login(username=self.username, password=self.password1)
        self.client.get(reverse('logout user confirmation'))

        response = self.client.post(reverse('logout user'))
        self.assertEqual(HTTPStatus.FOUND, response.status_code)

    def test_user_logout_successfully(self):
        self.client.login(username=self.username, password=self.password1)
        self.client.get(reverse('logout user confirmation'))

        response = self.client.post(reverse('logout user'))
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertRedirects(response, reverse('show home'))
        self.assertNotIn('_auth_user_id', self.client.session)
