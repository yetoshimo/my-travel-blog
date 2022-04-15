from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity, VisitedHotel, TravelEntry, TravelPicture

UserModel = get_user_model()


class EditTravelEntryViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.other_username = 'other_testuser'
        self.password1 = 'P@ssword1'
        self.context_data = 'located_city'
        self.city_name = 'sofia'
        self.other_city_name = 'shumen'
        self.country_name = 'bulgaria'
        self.title = 'Travel Entry Lorem Ipsum'
        self.other_title = 'Other Travel Entry Lorem Ipsum'
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

    def test_travel_entry_edit_with_no_travel_entry_page_url(self):
        response = self.client.get(f'/edit-travel-entry/{self.test_travel_entry_id}/')
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_travel_entry_edit_with_no_travel_entry_page_view_name(self):
        response = self.client.get(reverse('travel entry edit', kwargs={'pk': self.test_travel_entry_id}))
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_travel_entry_edit_with_existing_travel_entry_saves_changes_successfully(self):
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
        cities = VisitedCity.objects.filter(user=self.user).all()
        hotels = VisitedHotel.objects.filter(user=self.user).all()
        pictures = TravelPicture.objects.filter(user=self.user).all()
        self.assertEqual(1, VisitedCity.objects.filter(user=self.user).count())
        self.assertEqual(1, TravelEntry.objects.filter(user=self.user).count())

        data = {
            'travel_picture': '',
            'title': self.other_title,
            'description': '',
            'visited_city': visited_city.id,
            'visited_hotel': '',
        }
        response = self.client.post(reverse('travel entry edit', kwargs={'pk': travel_entry.id}),
                                    data=data,
                                    visited_city=cities,
                                    visited_hotel=hotels,
                                    travel_picture=pictures)
        self.assertRedirects(response,
                             reverse('travel entry details', kwargs={'pk': travel_entry.id}),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)
        travel_entry.refresh_from_db()
        self.assertEqual(self.other_title, travel_entry.title)
