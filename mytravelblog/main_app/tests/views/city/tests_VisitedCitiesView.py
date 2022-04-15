from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity

UserModel = get_user_model()


class VisitedCitiesViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.other_username = 'testuser2'
        self.password1 = 'P@ssword1'
        self.context_data = 'user_cities'
        self.city_name = 'sofia'
        self.other_city_name = 'shumen'
        self.country_name = 'bulgaria'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.user_two = UserModel.objects.create_user(
            username=self.other_username,
            password=self.password1,
        )

        self.client.login(username=self.username, password=self.password1)

    def test_cities_view_no_city_registered_page_url(self):
        response = self.client.get('/show-cities/')
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_cities_view_no_city_registered_age_view_name(self):
        response = self.client.get(reverse('cities view'))
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_cities_view_with_existing_city(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        self.assertEqual(1, VisitedCity.objects.count())
        response = self.client.get(reverse('cities view'))
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, 'main_app/generic/visited_cities.html')

    def test_cities_view_does_not_show_other_user_city(self):
        visited_city_one = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        visited_city_two = VisitedCity.objects.create(
            city_name=self.other_city_name,
            country_name=self.country_name,
            user=self.user_two,
        )
        self.assertEqual(2, VisitedCity.objects.count())
        response = self.client.get(reverse('cities view'))
        self.assertEqual(1, len(response.context_data['cities']))
        self.assertEqual(visited_city_one, response.context_data['cities'][0])
