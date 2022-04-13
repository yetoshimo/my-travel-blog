from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

UserModel = get_user_model()


class ChangeUserPasswordViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword2',
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

    def test_change_password_view_url(self):
        self.client.login(username=self.username, password=self.password1)

        response = self.client.get(f'/accounts/edit-password/{self.user.id}/')
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, template_name='accounts/change_password.html')

    def test_change_password_view_name(self):
        self.client.login(username=self.username, password=self.password1)

        response = self.client.get(reverse('change password', kwargs={'pk': self.user.id}))
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, template_name='accounts/change_password.html')

    def test_change_password_view_password_change(self):
        self.client.login(username=self.username, password=self.password1)

        data = {
            'old_password': self.password1,
            'new_password1': self.password2,
            'new_password2': self.password2,
        }

        response = self.client.post(reverse('change password', kwargs={'pk': self.user.id}), data=data)
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': self.user.id}))
