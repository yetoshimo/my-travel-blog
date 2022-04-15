from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity, VisitedHotel

UserModel = get_user_model()


class VisitedHotelsViewTests(django_tests.TestCase):
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

    def test_hotels_view_with_no_city_registered_page_url(self):
        response = self.client.get('/show-hotels/')
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_hotels_view_with_no_city_registered_view_name(self):
        response = self.client.get(reverse('hotels view'))
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_hotels_view_with_existing_city_no_hotels(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        self.assertEqual(1, VisitedCity.objects.filter(user=self.user).count())
        response = self.client.get(reverse('hotels view'))
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_hotels_view_with_existing_city_and_hotel(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        visited_hotel = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            number_of_stars=self.number_of_stars,
            located_city=visited_city,
            user=self.user,
        )
        response = self.client.get(reverse('hotels view'))
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_hotels_view_does_not_show_other_user_hotels(self):
        visited_city_one = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        visited_city_two = VisitedCity.objects.create(
            city_name=self.other_city_name,
            country_name=self.country_name,
            user=self.other_user,
        )
        visited_hotel_one = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            number_of_stars=self.number_of_stars,
            located_city=visited_city_one,
            user=self.user,
        )
        visited_hotel_two = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            number_of_stars=self.number_of_stars,
            located_city=visited_city_two,
            user=self.other_user,
        )
        self.assertEqual(2, VisitedCity.objects.count())
        response = self.client.get(reverse('hotels view'))
        self.assertEqual(1, len(response.context_data['hotels']))
        self.assertEqual(visited_hotel_one, response.context_data['hotels'][0])
