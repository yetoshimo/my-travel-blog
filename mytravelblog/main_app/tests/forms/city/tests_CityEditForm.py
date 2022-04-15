from django import test as django_tests

from mytravelblog.main_app.forms.city import *
from mytravelblog.main_app.models import *

UserModel = get_user_model()


class CityEditFormFormTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword2'
        self.city_name = 'sofia'
        self.city_name_update = 'shumen'
        self.country_name = 'bulgaria'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

    def test_city_edit_form_saves_with_valid_data(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )

        self.assertEqual(self.city_name.title(), visited_city.city_name)

        data = {
            'city_name': self.city_name_update,
            'country_name': self.country_name,
        }

        city_edit_form = CityEditForm(instance=visited_city, data=data, user=self.user)
        self.assertTrue(city_edit_form.is_valid())
        city_edit_form.save()
        self.assertEqual(self.city_name_update.title(), visited_city.city_name)

    def test_city_edit_form_cannot_save_duplicate_city_in_same_country(self):
        visited_city_one = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        visited_city_two = VisitedCity.objects.create(
            city_name=self.city_name_update,
            country_name=self.country_name,
            user=self.user,
        )
        self.assertNotEqual(visited_city_one.city_name, visited_city_two.city_name)
        data = {
            'city_name': self.city_name,
            'country_name': self.country_name,
        }
        city_edit_form = CityEditForm(instance=visited_city_two, data=data, user=self.user)
        self.assertFalse(city_edit_form.is_valid())
        self.assertEqual(f'{self.city_name.title()} in {self.country_name.title()} already exists!',
                         city_edit_form.errors['city_name'][0])
