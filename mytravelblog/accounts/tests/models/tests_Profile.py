from django import test as django_tests
from django.contrib.auth import get_user_model

from mytravelblog.accounts.models import Profile

UserModel = get_user_model()


class ProfileTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword1'

        self.profile_picture = 'test-profile-picture.jpg'

        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

        self.profile = Profile.objects.get(user=self.user)

    def test_profile_created_when_user_is_created(self):
        self.assertEqual(self.user, self.profile.user)

    def test_profile_str_returns_correct_string(self):
        self.assertEqual(f"{self.user}'s Profile", str(self.profile))

    def test_delete_user_deletes_profile(self):
        self.user.delete()
        self.assertEqual(0, UserModel.objects.all().count())
        self.assertEqual(0, Profile.objects.all().count())

    def test_delete_profile_deletes_user(self):
        self.profile.delete()
        self.assertEqual(0, UserModel.objects.all().count())
        self.assertEqual(0, Profile.objects.all().count())