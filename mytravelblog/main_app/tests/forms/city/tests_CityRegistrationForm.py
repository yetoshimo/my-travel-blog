from django import test as django_tests

from mytravelblog.main_app.forms.city import *
from mytravelblog.main_app.models import *

UserModel = get_user_model()


class CityRegistrationFormTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword2'
        self.city_name = 'sofia'
        self.country_name = 'bulgaria'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

    def test_city_form_correctly_saves_with_valid_data(self):
        data = {
            'city_name': self.city_name,
            'country_name': self.country_name,
        }

        city_form = CityRegistrationForm(data=data, user=self.user)
        self.assertTrue(city_form.is_valid())
        city_form.save()
        self.assertEqual(self.user, city_form.user)
        self.assertEqual(self.city_name.title(), city_form.cleaned_data['city_name'])

    def test_city_form_cannot_save_duplicate_city_in_country(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        data = {
            'city_name': self.city_name,
            'country_name': self.country_name,
        }
        city_form = CityRegistrationForm(data=data, user=self.user)
        self.assertFalse(city_form.is_valid())
        self.assertEqual(f'{self.city_name.title()} in {self.country_name.title()} already exists!',
                         city_form.errors['__all__'][0])
