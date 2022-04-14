from django import test as django_tests

from mytravelblog.main_app.forms.city import *
from mytravelblog.main_app.models import *

UserModel = get_user_model()


class CityDeleteFormTests(django_tests.TestCase):
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

    def test_city_delete_form_initiates_successfully(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        CityDeleteForm(instance=visited_city)
