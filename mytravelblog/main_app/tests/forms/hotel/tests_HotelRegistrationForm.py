from django import test as django_tests

from mytravelblog.main_app.forms.hotel import *
from mytravelblog.main_app.models import *

UserModel = get_user_model()


class HotelRegistrationFormTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword2'
        self.city_name = 'sofia'
        self.country_name = 'bulgaria'
        self.hotel_name = 'Grand Hotel Sofia'
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

    def test_hotel_form_correctly_saves_with_valid_data(self):
        data = {
            'hotel_name': self.hotel_name,
            'number_of_stars': self.number_of_stars,
            'located_city': self.located_city,
        }

        hotel_form = HotelRegistrationForm(user=self.user, data=data, located_city=self.cities)
        self.assertTrue(hotel_form.is_valid())
        hotel_form.save()
        self.assertEqual(self.user, hotel_form.user)
        self.assertEqual(self.hotel_name, hotel_form.cleaned_data['hotel_name'])
        self.assertEqual(self.number_of_stars, hotel_form.cleaned_data['number_of_stars'])
        self.assertEqual(self.located_city, hotel_form.cleaned_data['located_city'])
        self.assertEqual(1, VisitedHotel.objects.count())

    def test_hotel_form_cannot_save_duplicate_hotel_in_same_city_and_country(self):
        visited_hotel = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            located_city=self.located_city,
            number_of_stars=self.number_of_stars,
            user=self.user,
            star_count=self.star_count,
        )
        self.assertEqual(1, VisitedHotel.objects.count())
        data = {
            'hotel_name': self.hotel_name,
            'number_of_stars': self.number_of_stars,
            'located_city': self.located_city,
        }

        hotel_form = HotelRegistrationForm(user=self.user, data=data, located_city=self.cities)
        self.assertFalse(hotel_form.is_valid())
        self.assertEqual(f'{self.hotel_name} in {self.located_city} already exists!',
                         hotel_form.errors['__all__'][0])
