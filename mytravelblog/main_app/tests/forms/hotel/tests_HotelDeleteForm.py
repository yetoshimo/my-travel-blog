from django import test as django_tests

from mytravelblog.main_app.forms.hotel import *
from mytravelblog.main_app.models import *

UserModel = get_user_model()


class HotelDeleteFormTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword2'
        self.city_name = 'sofia'
        self.country_name = 'bulgaria'
        self.hotel_name = 'Grand Hotel Sofia'
        self.hotel_name_update = 'Silver Hotel'
        self.number_of_stars = '4'
        self.star_count = ''.join([str(i) for i in range(int(self.number_of_stars))])
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.located_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )

    def test_hotel_delete_form_initiates_successfully(self):
        visited_hotel = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            located_city=self.located_city,
            number_of_stars=self.number_of_stars,
            user=self.user,
            star_count=self.star_count,
        )
        self.assertEqual(1, VisitedHotel.objects.count())
        HotelDeleteForm(instance=visited_hotel)
