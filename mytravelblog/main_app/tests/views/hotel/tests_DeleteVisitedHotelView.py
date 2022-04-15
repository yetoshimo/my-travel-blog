from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity, VisitedHotel

UserModel = get_user_model()


class DeleteVisitedHotelViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.other_username = 'other_testuser'
        self.password1 = 'P@ssword1'
        self.context_data = 'located_city'
        self.city_name = 'sofia'
        self.other_city_name = 'shumen'
        self.country_name = 'bulgaria'
        self.hotel_name = 'Grand Hotel Sofia'
        self.other_hotel_name = 'Grand Hotel Shumen'
        self.number_of_stars = '4'
        self.test_visited_hotel_id = 10
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.other_user = UserModel.objects.create_user(
            username=self.other_username,
            password=self.password1,
        )

        self.client.login(username=self.username, password=self.password1)

    def test_delete_hotel_view_no_hotel_page_url(self):
        response = self.client.get(f'/delete-hotel/{self.test_visited_hotel_id}/')
        self.assertRedirects(response,
                             reverse('hotels view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_delete_hotel_view_no_hotel_view_name(self):
        response = self.client.get(reverse('hotel delete', kwargs={'pk': self.test_visited_hotel_id}))
        self.assertRedirects(response,
                             reverse('hotels view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_delete_hotel_view_with_existing_hotel(self):
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
        visited_city_other_user = VisitedCity.objects.create(
            city_name=self.other_city_name,
            country_name=self.country_name,
            user=self.other_user,
        )
        visited_hotel_other_user = VisitedHotel.objects.create(
            hotel_name=self.other_hotel_name,
            number_of_stars=self.number_of_stars,
            located_city=visited_city_other_user,
            user=self.other_user,
        )
        self.assertEqual(2, VisitedCity.objects.count())
        self.assertEqual(2, VisitedHotel.objects.count())
        response = self.client.post(reverse('hotel delete', kwargs={'pk': visited_hotel.id}))
        self.assertRedirects(response,
                             reverse('hotels view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)
        self.assertEqual(1, VisitedHotel.objects.count())
        self.assertEqual(0, VisitedHotel.objects.filter(user=self.user).count())
        self.assertEqual(1, VisitedHotel.objects.count())
        self.assertEqual(1, VisitedHotel.objects.filter(user=self.other_user).count())
