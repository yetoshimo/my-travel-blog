from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.urls import reverse

from mytravelblog.main_app.models import VisitedCity, VisitedHotel, TravelPicture

UserModel = get_user_model()


class EditTravelPictureViewTests(django_tests.TestCase):
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

    def test_edit_travel_picture_no_travel_picture_registered_page_url(self):
        response = self.client.get(f'/edit-travel-picture/{self.test_travel_picture_id}/')
        self.assertRedirects(response,
                             reverse('travel pictures view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_edit_travel_picture_no_travel_picture_registered_page_view_name(self):
        response = self.client.get(reverse('travel picture edit', kwargs={'pk': self.test_travel_picture_id}))
        self.assertRedirects(response,
                             reverse('travel pictures view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.FOUND)

    def test_edit_travel_picture_with_existing_hotel_saves_changes_successfully(self):
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
        cities = VisitedCity.objects.filter(user=self.user).all()
        self.assertEqual(1, VisitedCity.objects.filter(user=self.user).count())
        data = {
            # 'travel_picture': self.travel_picture,
            'title': self.other_title,
            'located_city': visited_city.pk,
        }
        response = self.client.post(reverse('travel picture edit', kwargs={'pk': travel_picture.id}),
                                    data=data,
                                    located_city=cities)
        self.assertRedirects(response,
                             reverse('travel pictures view'),
                             status_code=HTTPStatus.FOUND,
                             target_status_code=HTTPStatus.OK)
        travel_picture.refresh_from_db()
        self.assertEqual(self.other_title, travel_picture.title)

    def test_edit_travel_picture_cannot_save_duplicate_title_for_same_user(self):
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
        data = {
            # 'travel_picture': self.travel_picture,
            'title': self.title,
            'located_city': visited_city.pk,
        }
        cities = VisitedCity.objects.filter(user=self.user).all()
        response = self.client.post(reverse('travel picture edit', kwargs={'pk': travel_picture_two.id}),
                                    data=data,
                                    located_city=cities)
        self.assertEqual(f'Picture with title "{self.title}" already exists!',
                         response.context_data['form'].errors['title'][0])
