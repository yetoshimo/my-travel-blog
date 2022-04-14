from django import test as django_tests
from django.contrib.auth import get_user_model

from mytravelblog.main_app.models import VisitedCity, TravelPicture

UserModel = get_user_model()


class TravelPictureTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword2'
        self.city_name = 'sofia'
        self.country_name = 'bulgaria'
        self.travel_picture = 'test-picture.jpg'
        self.title = 'Picture Lorem Ipsum'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.located_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )

    def test_travel_picture_returns_correct_string(self):
        travel_picture = TravelPicture.objects.create(
            travel_picture=self.travel_picture,
            title=self.title,
            located_city=self.located_city,
            user=self.user,
        )
        self.assertEqual(f'{self.title}, {self.located_city}', str(travel_picture))
