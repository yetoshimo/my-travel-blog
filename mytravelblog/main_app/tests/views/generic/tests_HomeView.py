from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

UserModel = get_user_model()


class HomeViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.other_username = 'testuser2'
        self.password1 = 'P@ssword1'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

    def test_home_view_if_user_is_not_authenticated(self):
        response = self.client.get('')
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, 'main_app/generic/home.html')

    def test_home_view_if_user_is_authenticated(self):
        self.client.login(username=self.username, password=self.password1)
        response = self.client.get('')
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)
