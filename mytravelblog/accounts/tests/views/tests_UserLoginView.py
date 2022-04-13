from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.accounts.views import UserLoginView

UserModel = get_user_model()


class UserLoginViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

    def test_user_login_page_url(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, template_name='accounts/login_page.html')

    def test_user_registration_page_view_name(self):
        response = self.client.get(reverse('login user'))
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, template_name='accounts/login_page.html')

    def test_user_login_with_valid_data(self):
        response = self.client.post(
            reverse('login user'),
            data={
                'username': self.username,
                'password': self.password1,
            }
        )
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertRedirects(response, reverse('show dashboard'))

    def test_user_login_without_success_url(self):
        UserLoginView.success_url = ''

        response = self.client.post(
            reverse('login user'),
            data={
                'username': self.username,
                'password': self.password1,
            }
        )

        self.assertRedirects(response,
                             '/accounts/profile/',
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.NOT_FOUND)
