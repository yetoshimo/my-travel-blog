from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity, VisitedHotel

UserModel = get_user_model()


class EditVisitedHotelViewTests(django_tests.TestCase):
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

    def test_edit_hotel_no_hotel_registered_page_url(self):
        response = self.client.get(f'/edit-hotel/{self.test_visited_hotel_id}/')
        self.assertRedirects(response,
                             reverse('hotels view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_edit_hotel_no_hotel_registered_page_view_name(self):
        response = self.client.get(reverse('hotel edit', kwargs={'pk': self.test_visited_hotel_id}))
        self.assertRedirects(response,
                             reverse('hotels view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_edit_hotel_with_existing_hotel_saves_changes_successfully(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        visited_city_other_user = VisitedCity.objects.create(
            city_name=self.other_city_name,
            country_name=self.country_name,
            user=self.other_user,
        )
        self.assertEqual(1, VisitedCity.objects.filter(user=self.user).count())
        cities = VisitedCity.objects.filter(user=self.user).all()

        visited_hotel = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            located_city=visited_city,
            number_of_stars=self.number_of_stars,
            user=self.user,
        )
        self.assertEqual(1, VisitedHotel.objects.filter(user=self.user).count())

        data = {
            'hotel_name': self.other_hotel_name,
            'number_of_stars': self.number_of_stars,
            'located_city': visited_city.pk,
        }

        response = self.client.post(reverse('hotel edit', kwargs={'pk': visited_hotel.id}),
                                    data=data,
                                    located_city=cities)
        self.assertRedirects(response,
                             reverse('hotels view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)
        visited_hotel.refresh_from_db()
        self.assertEqual(self.other_hotel_name, visited_hotel.hotel_name)

    def test_edit_hotel_cannot_save_duplicate_hotel_in_same_city(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        visited_hotel = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            located_city=visited_city,
            number_of_stars=self.number_of_stars,
            user=self.user,
        )
        visited_hotel_two = VisitedHotel.objects.create(
            hotel_name=self.other_hotel_name,
            located_city=visited_city,
            number_of_stars=self.number_of_stars,
            user=self.user,
        )
        self.assertEqual(2, VisitedHotel.objects.filter(user=self.user).count())
        cities = VisitedCity.objects.filter(user=self.user).all()

        data = {
            'hotel_name': self.hotel_name,
            'number_of_stars': self.number_of_stars,
            'located_city': visited_city.pk,
        }

        response = self.client.post(reverse('hotel edit', kwargs={'pk': visited_hotel_two.id}),
                                    data=data,
                                    located_city=cities)
        self.assertEqual(f'{self.hotel_name} in {visited_city} already exists!',
                         response.context_data['form'].errors['hotel_name'][0])
