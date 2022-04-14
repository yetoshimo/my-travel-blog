from django import test as django_tests
from django.contrib.auth import get_user_model

from mytravelblog.main_app.models import *

UserModel = get_user_model()


class TravelEntryTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword2'
        self.city_name = 'sofia'
        self.country_name = 'bulgaria'
        self.title = 'Travel Entry Lorem Ipsum'
        self.description = 'Lorem ipsum'
        self.hotel_name = 'Grand Hotel Sofia'
        self.number_of_stars = '4'
        self.travel_picture = 'test-picture.jpg'
        self.title = 'Picture Lorem Ipsum'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        self.visited_hotel = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            number_of_stars=self.number_of_stars,
            located_city=self.visited_city,
            user=self.user,
        )
        self.travel_picture = TravelPicture.objects.create(
            travel_picture=self.travel_picture,
            title=self.title,
            located_city=self.visited_city,
            user=self.user,
        )

    def test_travel_entry_returns_correct_string(self):
        travel_entry = TravelEntry.objects.create(
            title=self.title,
            description=self.description,
            visited_city=self.visited_city,
            visited_hotel=self.visited_hotel,
            travel_picture=self.travel_picture,
            user=self.user,
        )
        self.assertEqual(f'{self.title}, {self.visited_city}', str(travel_entry))
