from django import test as django_tests

from mytravelblog.main_app.forms.hotel import *
from mytravelblog.main_app.models import *

UserModel = get_user_model()


class HotelEditFormTests(django_tests.TestCase):
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

        self.cities = VisitedCity.objects.filter(user=self.user).all()

    def test_hotel_edit_form_saves_with_valid_data(self):
        visited_hotel = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            located_city=self.located_city,
            number_of_stars=self.number_of_stars,
            user=self.user,
            star_count=self.star_count,
        )

        self.assertEqual(1, VisitedHotel.objects.count())

        data = {
            'hotel_name': self.hotel_name_update,
            'number_of_stars': self.number_of_stars,
            'located_city': self.located_city,
        }

        hotel_edit_form = HotelEditForm(instance=visited_hotel, data=data, user=self.user, located_city=self.cities)

        self.assertTrue(hotel_edit_form.is_valid())
        hotel_edit_form.save()
        self.assertEqual(self.hotel_name_update, visited_hotel.hotel_name)

    def test_hotel_edit_form_cannot_save_duplicate_hotel_in_same_city_and_country(self):
        visited_hotel_one = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            located_city=self.located_city,
            number_of_stars=self.number_of_stars,
            user=self.user,
            star_count=self.star_count,
        )
        visited_hotel_two = VisitedHotel.objects.create(
            hotel_name=self.hotel_name_update,
            located_city=self.located_city,
            number_of_stars=self.number_of_stars,
            user=self.user,
            star_count=self.star_count,
        )
        self.assertNotEqual(visited_hotel_one.hotel_name, visited_hotel_two.hotel_name)
        self.assertEqual(visited_hotel_one.located_city, visited_hotel_two.located_city)
        data = {
            'hotel_name': self.hotel_name,
            'number_of_stars': self.number_of_stars,
            'located_city': self.located_city,
        }

        hotel_edit_form = HotelEditForm(instance=visited_hotel_two, data=data, user=self.user, located_city=self.cities)
        self.assertFalse(hotel_edit_form.is_valid())
        self.assertEqual(f'{self.hotel_name} in {self.located_city} already exists!',
                         hotel_edit_form.errors['hotel_name'][0])
