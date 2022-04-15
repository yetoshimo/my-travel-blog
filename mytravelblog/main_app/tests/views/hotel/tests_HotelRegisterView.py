from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity, VisitedHotel

UserModel = get_user_model()


class HotelRegisterViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.other_username = 'other_testuser'
        self.password1 = 'P@ssword1'
        self.context_data = 'located_city'
        self.city_name = 'sofia'
        self.other_city_name = 'shumen'
        self.country_name = 'bulgaria'
        self.hotel_name = 'Grand Hotel Sofia'
        self.number_of_stars = '4'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.other_user = UserModel.objects.create_user(
            username=self.other_username,
            password=self.password1,
        )

        self.client.login(username=self.username, password=self.password1)

    def test_hotel_registration_with_no_city(self):
        response = self.client.get('/register-hotel/')
        self.assertRedirects(response,
                             reverse('register city'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_hotel_registration_view_no_city_view_name(self):
        response = self.client.get(reverse('register hotel'))
        self.assertRedirects(response,
                             reverse('register city'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_hotel_registration_view_with_city_of_other_user(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.other_user,
        )
        self.assertEqual(0, VisitedCity.objects.filter(user=self.user).count())
        response = self.client.get(reverse('register hotel'))
        self.assertRedirects(response,
                             reverse('register city'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_hotel_registration_view_with_city(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        visited_city_other_user = VisitedCity.objects.create(
            city_name=self.other_city_name,
            country_name=self.country_name,
            user=self.other_user,
        )
        self.assertEqual(1, VisitedCity.objects.filter(user=self.user).count())
        response = self.client.get(reverse('register hotel'))
        self.assertEqual(self.user, response.context_data['form'].user)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertNotIn(visited_city_other_user, response.context_data['form']['located_city'])

    def test_hotel_registration_saves_with_valid_city_and_redirects(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )

        cities = VisitedCity.objects.filter(user=self.user).all()
        self.assertEqual(1, VisitedCity.objects.filter(user=self.user).count())
        data = {
            'hotel_name': self.hotel_name,
            'number_of_stars': self.number_of_stars,
            'located_city': visited_city.pk,
        }
        self.assertEqual(0, VisitedHotel.objects.count())

        response = self.client.post(reverse('register hotel'),
                                    data=data,
                                    located_city=cities)
        self.assertRedirects(response,
                             reverse('hotels view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)
        self.assertEqual(1, VisitedHotel.objects.count())

    def test_hotel_registration_cannot_save_duplicate_hotel_in_same_city(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        cities = VisitedCity.objects.filter(user=self.user).all()
        self.assertEqual(1, VisitedCity.objects.filter(user=self.user).count())
        visited_hotel = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            located_city=visited_city,
            number_of_stars=self.number_of_stars,
            user=self.user,
        )
        self.assertEqual(1, VisitedHotel.objects.filter(user=self.user).count())
        data = {
            'hotel_name': self.hotel_name,
            'number_of_stars': self.number_of_stars,
            'located_city': visited_city.pk,
        }
        response = self.client.post(reverse('register hotel'),
                                    data=data,
                                    located_city=cities)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(f'{self.hotel_name} in {visited_city} already exists!',
                         response.context_data['form'].errors['hotel_name'][0])
