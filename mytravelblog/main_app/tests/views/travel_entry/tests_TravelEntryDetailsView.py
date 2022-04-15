from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity, VisitedHotel, TravelEntry

UserModel = get_user_model()


class TravelEntryDetailsViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.other_username = 'other_testuser'
        self.password1 = 'P@ssword1'
        self.context_data = 'located_city'
        self.city_name = 'sofia'
        self.other_city_name = 'shumen'
        self.country_name = 'bulgaria'
        self.title = 'Travel Entry Lorem Ipsum'
        self.description = 'Lorem ipsum'
        self.test_travel_entry_id = 10
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.other_user = UserModel.objects.create_user(
            username=self.other_username,
            password=self.password1,
        )

        self.client.login(username=self.username, password=self.password1)

    def test_travel_entry_details_with_no_travel_entry_page_url(self):
        response = self.client.get(f'/travel-entry-view/{self.test_travel_entry_id}/')
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_travel_entry_details_with_no_travel_entry_page_view_name(self):
        response = self.client.get(reverse('travel entry details', kwargs={'pk': self.test_travel_entry_id}))
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_travel_entry_details_with_existing_travel_detail(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        travel_entry = TravelEntry.objects.create(
            title=self.title,
            description=self.description,
            visited_city=visited_city,
            user=self.user,
        )
        response = self.client.get(reverse('travel entry details', kwargs={'pk': travel_entry.id}))
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(str(travel_entry), str(response.context_data['travel_entry']))
