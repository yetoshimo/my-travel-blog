from django import test as django_tests
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from mytravelblog.main_app.models import VisitedCity, VisitedHotel

UserModel = get_user_model()


class VisitedHotelTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword2'
        self.city_name = 'sofia'
        self.country_name = 'bulgaria'
        self.hotel_name = 'Grand Hotel Sofia'
        self.number_of_stars = '4'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.located_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )

    def test_visited_hotel_returns_correct_string(self):
        visited_hotel = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            number_of_stars=self.number_of_stars,
            located_city=self.located_city,
            user=self.user,
        )
        self.assertEqual(f'{self.hotel_name}, {self.located_city}', str(visited_hotel))
        self.assertEqual(int(self.number_of_stars), len(visited_hotel.star_count))

    def test_user_cannot_register_duplicate_hotel_in_same_city(self):
        number_of_hotels = 0
        with self.assertRaises(Exception) as context:
            visited_hotel = VisitedHotel.objects.create(
                hotel_name=self.hotel_name,
                number_of_stars=self.number_of_stars,
                located_city=self.located_city,
                user=self.user,
            )
            number_of_hotels = VisitedCity.objects.all().count()
            visited_hotel_invalid = VisitedHotel.objects.create(
                hotel_name=self.hotel_name,
                number_of_stars=self.number_of_stars,
                located_city=self.located_city,
                user=self.user,
            )
        self.assertEqual(1, number_of_hotels)
        self.assertEqual(IntegrityError, type(context.exception))
