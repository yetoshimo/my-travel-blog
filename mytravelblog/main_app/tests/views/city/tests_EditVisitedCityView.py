from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity

UserModel = get_user_model()


class EditVisitedCityViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.other_username = 'other_testuser'
        self.password1 = 'P@ssword1'
        self.context_data = 'user_cities'
        self.city_name = 'sofia'
        self.other_city_name = 'shumen'
        self.country_name = 'bulgaria'
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

    def test_edit_city_view_no_city_registered_page_url(self):
        response = self.client.get(f'/edit-city/{self.test_visited_city_id}/')
        self.assertRedirects(response,
                             reverse('cities view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_edit_city_view_no_city_registered_age_view_name(self):
        response = self.client.get(reverse('city edit', kwargs={'pk': self.test_visited_city_id}))
        self.assertRedirects(response,
                             reverse('cities view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_edit_city_view_with_existing_city(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        self.assertEqual(1, VisitedCity.objects.filter(user=self.user).count())
        response = self.client.get(reverse('city edit', kwargs={'pk': visited_city.id}))
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(self.user, response.context_data['form'].user)

    def test_user_cannot_access_other_user_city(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.other_user,
        )
        self.assertEqual(0, VisitedCity.objects.filter(user=self.user).count())
        self.assertEqual(1, VisitedCity.objects.filter(user=self.other_user).count())
        response = self.client.get(reverse('city edit', kwargs={'pk': visited_city.id}))
        self.assertRedirects(response,
                             reverse('cities view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_edit_city_view_saves_changes_successfully(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        self.assertEqual(1, VisitedCity.objects.filter(user=self.user).count())
        data = {
            'city_name': self.other_city_name,
            'country_name': self.country_name,
        }
        response = self.client.post(reverse('city edit', kwargs={'pk': visited_city.id}),
                                    data=data)
        self.assertRedirects(response,
                             reverse('cities view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)
        visited_city.refresh_from_db()
        self.assertEqual(self.other_city_name.title(), visited_city.city_name)

    def test_edit_city_view_cannot_save_duplicate_city_in_same_country(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        visited_city_two = VisitedCity.objects.create(
            city_name=self.other_city_name,
            country_name=self.country_name,
            user=self.user,
        )
        self.assertEqual(2, VisitedCity.objects.filter(user=self.user).count())
        data = {
            'city_name': self.city_name,
            'country_name': self.country_name,
        }
        response = self.client.post(reverse('city edit', kwargs={'pk': visited_city_two.id}),
                                    data=data)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(f'{self.city_name.title()} in {self.country_name.title()} already exists!',
                         response.context_data['form'].errors['city_name'][0])
