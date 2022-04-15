from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.accounts.models import Profile

UserModel = get_user_model()


class UserProfileDetailsView(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.username2 = 'testuser2'
        self.password2 = 'P@ssword2'
        self.user2 = UserModel.objects.create_user(
            username=self.username2,
            password=self.password2,
        )

        self.client.login(username=self.username, password=self.password1)

    def test_user_can_access_own_profile_details(self):
        response = self.client.get(reverse('profile details', kwargs={'pk': self.user.id}))
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_user_cannot_access_other_profile(self):
        response = self.client.get(reverse('profile details', kwargs={'pk': self.user2.id}))
        self.assertRedirects(response,
                             reverse('profile details', kwargs={'pk': self.user.id}),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)
