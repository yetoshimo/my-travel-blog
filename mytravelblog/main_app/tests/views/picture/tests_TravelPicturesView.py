from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity, VisitedHotel, TravelPicture

UserModel = get_user_model()


class TravelPicturesViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.other_username = 'other_testuser'
        self.password1 = 'P@ssword1'
        self.context_data = 'located_city'
        self.city_name = 'sofia'
        self.other_city_name = 'shumen'
        self.country_name = 'bulgaria'
        self.title = 'Picture Lorem Ipsum'
        self.travel_picture = 'test-picture.png'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.other_user = UserModel.objects.create_user(
            username=self.other_username,
            password=self.password1,
        )

        self.client.login(username=self.username, password=self.password1)

    def test_travel_pictures_view_with_no_city_registered_page_url(self):
        response = self.client.get('/show-travel-pictures/')
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_travel_pictures_with_no_city_registered_view_name(self):
        response = self.client.get(reverse('travel pictures view'))
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_travel_pictures_with_existing_city_no_hotels(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        self.assertEqual(1, VisitedCity.objects.filter(user=self.user).count())
        response = self.client.get(reverse('travel pictures view'))
        self.assertRedirects(response,
                             reverse('show dashboard'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)

    def test_travel_pictures_view_with_existing_city_and_travel_picture(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        travel_picture = TravelPicture.objects.create(
            # travel_picture=self.travel_picture,
            title=self.title,
            located_city=visited_city,
            user=self.user,
        )
        response = self.client.get(reverse('travel pictures view'))
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_travel_pictures_view_does_not_show_other_user_travel_pictures(self):
        visited_city_one = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        visited_city_two = VisitedCity.objects.create(
            city_name=self.other_city_name,
            country_name=self.country_name,
            user=self.other_user,
        )
        travel_picture_one = TravelPicture.objects.create(
            # travel_picture=self.travel_picture,
            title=self.title,
            located_city=visited_city_one,
            user=self.user,
        )
        travel_picture_two = TravelPicture.objects.create(
            # travel_picture=self.travel_picture,
            title=self.title,
            located_city=visited_city_two,
            user=self.other_user,
        )
        self.assertEqual(2, TravelPicture.objects.count())
        response = self.client.get(reverse('travel pictures view'))
        self.assertEqual(1, len(response.context_data['travel_pictures']))
        self.assertEqual(travel_picture_one, response.context_data['travel_pictures'][0])
