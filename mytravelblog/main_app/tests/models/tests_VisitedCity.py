from django import test as django_tests
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from mytravelblog.main_app.models import VisitedCity

UserModel = get_user_model()


class VisitedCityTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword2'
        self.city_name = 'sofia'
        self.country_name = 'bulgaria'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

    def test_visited_city_returns_correct_string(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )

        self.assertEqual(f'{self.city_name.title()}, {self.country_name.title()}', str(visited_city))

    def test_user_cannot_register_duplicate_city_in_same_country(self):
        number_of_cities = 0
        with self.assertRaises(Exception) as context:
            visited_city = VisitedCity.objects.create(
                city_name=self.city_name,
                country_name=self.country_name,
                user=self.user,
            )
            number_of_cities = VisitedCity.objects.all().count()
            visited_city_invalid = VisitedCity.objects.create(
                city_name=self.city_name,
                country_name=self.country_name,
                user=self.user,
            )
        self.assertEqual(1, number_of_cities)
        self.assertEqual(IntegrityError, type(context.exception))
