from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity, VisitedHotel, TravelPicture

UserModel = get_user_model()


class DeleteTravelPictureViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.other_username = 'other_testuser'
        self.password1 = 'P@ssword1'
        self.context_data = 'located_city'
        self.city_name = 'sofia'
        self.other_city_name = 'shumen'
        self.country_name = 'bulgaria'
        self.title = 'Picture Lorem Ipsum'
        self.other_title = 'Ohter Picture Lorem Ipsum'
        self.travel_picture = 'test-picture.png'
        self.test_travel_picture_id = 10
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.other_user = UserModel.objects.create_user(
            username=self.other_username,
            password=self.password1,
        )

        self.client.login(username=self.username, password=self.password1)

    def test_delete_travel_picture_view_no_travel_picture_page_url(self):
        response = self.client.get(f'/delete-travel-picture/{self.test_travel_picture_id}/')
        self.assertRedirects(response,
                             reverse('travel pictures view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_delete_travel_picture_no_travel_picture_view_name(self):
        response = self.client.get(reverse('travel picture delete', kwargs={'pk': self.test_travel_picture_id}))
        self.assertRedirects(response,
                             reverse('travel pictures view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_delete_travel_picture_with_existing_picture(self):
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
        travel_picture_two = TravelPicture.objects.create(
            # travel_picture=self.travel_picture,
            title=self.other_title,
            located_city=visited_city,
            user=self.user,
        )
        self.assertEqual(2, TravelPicture.objects.filter(user=self.user).count())

        response = self.client.post(reverse('travel picture delete', kwargs={'pk': travel_picture_two.id}))
        self.assertRedirects(response,
                             reverse('travel pictures view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)
        self.assertEqual(1, TravelPicture.objects.filter(user=self.user).count())
        self.assertFalse(TravelPicture.objects.filter(user=self.user, title=self.other_title).exists())
