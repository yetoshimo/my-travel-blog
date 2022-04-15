from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity

UserModel = get_user_model()


class CityRegisterViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.context_data = 'user_cities'
        self.city_name = 'sofia'
        self.country_name = 'bulgaria'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

        self.client.login(username=self.username, password=self.password1)

    def test_city_registration_page_url(self):
        response = self.client.get('/register-city/')
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, template_name='main_app/city/city_create.html')

    def test_city_registration_page_view_name(self):
        response = self.client.get(reverse('register city'))
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, template_name='main_app/city/city_create.html')

    def test_city_registration_view_has_user_cities_context(self):
        response = self.client.get(reverse('register city'))
        self.assertIn(self.context_data, response.context)

    def test_city_registration_view_has_user_form_value(self):
        response = self.client.get(reverse('register city'))
        self.assertEqual(self.user, response.context_data['form'].user)

    def test_city_registration_view_saves_valid_city_and_redirects(self):
        data = {
            'city_name': self.city_name,
            'country_name': self.country_name,
        }
        response = self.client.post(reverse('register city'), data=data)
        self.assertRedirects(response,
                             reverse('cities view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)
        self.assertEqual(1, VisitedCity.objects.count())

    def test_city_registration_user_cannot_save_duplicate_city_in_same_country(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        self.assertEqual(1, VisitedCity.objects.count())
        data = {
            'city_name': self.city_name,
            'country_name': self.country_name,
        }
        response = self.client.post(reverse('register city'), data=data)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(f'{self.city_name.title()} in {self.country_name.title()} already exists!',
                         response.context_data['form'].errors['city_name'][0])
