from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

UserModel = get_user_model()


class UserLogoutConfirmationViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

    def test_user_logout_confirmation_page_url(self):
        self.client.login(username=self.username, password=self.password1)

        response = self.client.get('/accounts/logout/')
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, template_name='accounts/logout_page.html')

    def test_user_logout_confirmation_page_view_name(self):
        self.client.login(username=self.username, password=self.password1)

        response = self.client.get(reverse('logout user confirmation'))
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, template_name='accounts/logout_page.html')
