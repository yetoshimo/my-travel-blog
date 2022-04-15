from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity, VisitedHotel

UserModel = get_user_model()


class DeleteVisitedCityTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.other_username = 'other_testuser'
        self.password1 = 'P@ssword1'
        self.context_data = 'user_cities'
        self.city_name = 'sofia'
        self.other_city_name = 'shumen'
        self.country_name = 'bulgaria'
        self.hotel_name = 'Grand Hotel Sofia'
        self.number_of_stars = '4'
        self.test_visited_city_id = 10
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.other_user = UserModel.objects.create_user(
            username=self.other_username,
            password=self.password1,
        )

        self.client.login(username=self.username, password=self.password1)

    def test_delete_city_view_no_city_page_url(self):
        response = self.client.get(f'/delete-city/{self.test_visited_city_id}/')
        self.assertRedirects(response,
                             reverse('cities view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_delete_city_view_no_city_view_name(self):
        response = self.client.get(reverse('city delete', kwargs={'pk': self.test_visited_city_id}))
        self.assertRedirects(response,
                             reverse('cities view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_delete_city_view_with_existing_city(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        self.assertEqual(1, VisitedCity.objects.filter(user=self.user).count())
        response = self.client.get(reverse('city delete', kwargs={'pk': visited_city.id}))
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_delete_city_view_user_cannot_access_other_user_city(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.other_user,
        )
        self.assertEqual(0, VisitedCity.objects.filter(user=self.user).count())
        self.assertEqual(1, VisitedCity.objects.filter(user=self.other_user).count())
        response = self.client.get(reverse('city delete', kwargs={'pk': visited_city.id}))
        self.assertRedirects(response,
                             reverse('cities view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_delete_view_deletes_city_and_related_objects_successfully(self):
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
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.other_user,
        )
        visited_hotel_other_user = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            number_of_stars=self.number_of_stars,
            located_city=visited_city_other_user,
            user=self.other_user,
        )
        self.assertEqual(2, VisitedCity.objects.count())
        self.assertEqual(2, VisitedHotel.objects.count())
        response = self.client.post(reverse('city delete', kwargs={'pk': visited_city.id}))
        self.assertRedirects(response,
                             reverse('cities view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)
        self.assertEqual(1, VisitedCity.objects.count())
        self.assertEqual(0, VisitedCity.objects.filter(user=self.user).count())
        self.assertEqual(1, VisitedHotel.objects.count())
        self.assertEqual(1, VisitedCity.objects.filter(user=self.other_user).count())
