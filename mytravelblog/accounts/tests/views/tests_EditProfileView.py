from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.accounts.models import Profile

UserModel = get_user_model()


class EditProfileViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.first_name = 'testuser-firstname'
        self.last_name = 'testuser-lastname'
        self.email = 'testuser@email.com'
        self.current_country = 'Bulgaria'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

    def test_edit_profile_view_url(self):
        self.client.login(username=self.username, password=self.password1)

        response = self.client.get(f'/accounts/edit-profile/{self.user.id}/')
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, template_name='accounts/profile/profile_edit.html')

    def test_edit_profile_view_name(self):
        self.client.login(username=self.username, password=self.password1)

        response = self.client.get(reverse('profile edit', kwargs={'pk': self.user.id}))
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(self.user, response.context['user'])
        self.assertTemplateUsed(response, template_name='accounts/profile/profile_edit.html')

    def test_edit_profile_view_successful_redirect(self):
        self.client.login(username=self.username, password=self.password1)

        response = self.client.post(reverse('profile edit', kwargs={'pk': self.user.id}))
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': self.user.id}))
