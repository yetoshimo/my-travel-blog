import os.path
from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

import cloudinary.uploader

from mytravelblog.main_app.models import VisitedCity, VisitedHotel, TravelPicture
from mytravelblog.settings import BASE_DIR

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

    def test_edit_travel_picture_cannot_save_duplicate_title_for_same_user_in_same_city(self):
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
        self.assertEqual(f'Picture with title "{self.title}" in {visited_city} already exists!',
                         response.context_data['form'].errors['title'][0])

    def test_edit_travel_picture_upload_picture(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        cities = VisitedCity.objects.filter(user=self.user).all()
        travel_picture = TravelPicture.objects.create(
            # travel_picture=self.travel_picture,
            title=self.title,
            located_city=visited_city,
            user=self.user,
        )
        self.assertFalse(travel_picture.travel_picture)
        with open(os.path.join(BASE_DIR,
                               'staticfiles',
                               'default_files',
                               'default_world_picture.png'), 'rb') as cloudinary_travel_picture:
            data = {
                'title': self.title,
                'travel_picture': SimpleUploadedFile(
                    name='default_world_picture.png',
                    content=cloudinary_travel_picture.read(),
                    content_type='image/png',
                ),
                'located_city': visited_city.pk,
            }
            response = self.client.post(reverse('travel picture edit',
                                                kwargs={'pk': travel_picture.pk}),
                                        data=data,
                                        located_city=cities,
                                        user=self.user)
            travel_picture.refresh_from_db()
            self.assertTrue(travel_picture.travel_picture)
            cloudinary.uploader.destroy(travel_picture.travel_picture.public_id, invalidate=True, )

    def test_edit_travel_picture_update_existing_picture(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        cities = VisitedCity.objects.filter(user=self.user).all()
        travel_picture = TravelPicture.objects.create(
            # travel_picture=self.travel_picture,
            title=self.title,
            located_city=visited_city,
            user=self.user,
        )
        with open(os.path.join(BASE_DIR,
                               'staticfiles',
                               'default_files',
                               'default_world_picture.png'), 'rb') as cloudinary_travel_picture:
            data = {
                'title': self.title,
                'travel_picture': SimpleUploadedFile(
                    name='default_world_picture.png',
                    content=cloudinary_travel_picture.read(),
                    content_type='image/png',
                ),
                'located_city': visited_city.pk,
            }
            self.client.post(reverse('travel picture edit',
                                     kwargs={'pk': travel_picture.pk}),
                             data=data,
                             located_city=cities,
                             user=self.user)
            travel_picture.refresh_from_db()
            old_public_id = travel_picture.travel_picture.public_id
            with open(os.path.join(BASE_DIR,
                                   'staticfiles',
                                   'default_files',
                                   'default_profile_picture.png'), 'rb') as cloudinary_travel_picture2:
                data = {
                    'title': self.title,
                    'travel_picture': SimpleUploadedFile(
                        name='default_profile_picture.png',
                        content=cloudinary_travel_picture2.read(),
                        content_type='image/png',
                    ),
                    'located_city': visited_city.pk,
                }
                response = self.client.post(reverse('travel picture edit',
                                                    kwargs={'pk': travel_picture.pk}),
                                            data=data,
                                            located_city=cities,
                                            user=self.user)
                travel_picture.refresh_from_db()
                new_public_id = travel_picture.travel_picture.public_id
                self.assertNotEqual(old_public_id, new_public_id)
                cloudinary.uploader.destroy(old_public_id, invalidate=True, )
                cloudinary.uploader.destroy(new_public_id, invalidate=True, )

    def test_travel_picture_clear_existing(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        cities = VisitedCity.objects.filter(user=self.user).all()
        travel_picture = TravelPicture.objects.create(
            # travel_picture=self.travel_picture,
            title=self.title,
            located_city=visited_city,
            user=self.user,
        )
        self.assertFalse(travel_picture.travel_picture)
        with open(os.path.join(BASE_DIR,
                               'staticfiles',
                               'default_files',
                               'default_world_picture.png'), 'rb') as cloudinary_travel_picture:
            data = {
                'title': self.title,
                'travel_picture': SimpleUploadedFile(
                    name='default_world_picture.png',
                    content=cloudinary_travel_picture.read(),
                    content_type='image/png',
                ),
                'located_city': visited_city.pk,
            }
            self.client.post(reverse('travel picture edit',
                                     kwargs={'pk': travel_picture.pk}),
                             data=data,
                             located_city=cities,
                             user=self.user)
            travel_picture.refresh_from_db()
            old_public_id = travel_picture.travel_picture.public_id
            data2 = {
                'title': self.title,
                'travel_picture-clear': 'on',
                'located_city': visited_city.pk,
            }
            response = self.client.post(reverse('travel picture edit',
                                                kwargs={'pk': travel_picture.pk}),
                                        data=data2,
                                        located_city=cities,
                                        user=self.user)
            travel_picture.refresh_from_db()
            self.assertFalse(travel_picture.travel_picture)
            cloudinary.uploader.destroy(old_public_id, invalidate=True, )

    def test_travel_picture_error_on_too_big_file(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        cities = VisitedCity.objects.filter(user=self.user).all()
        travel_picture = TravelPicture.objects.create(
            # travel_picture=self.travel_picture,
            title=self.title,
            located_city=visited_city,
            user=self.user,
        )
        self.assertFalse(travel_picture.travel_picture)
        with open(os.path.join(BASE_DIR,
                               'staticfiles',
                               'default_files',
                               'default_big_file.jpg'), 'rb') as cloudinary_travel_picture:
            data = {
                'title': self.title,
                'travel_picture': SimpleUploadedFile(
                    name='default_big_file.jpg',
                    content=cloudinary_travel_picture.read(),
                    content_type='image/png',
                ),
                'located_city': visited_city.pk,
            }
            response = self.client.post(reverse('travel picture edit',
                                                kwargs={'pk': travel_picture.pk}),
                                        data=data,
                                        located_city=cities,
                                        user=self.user)
            travel_picture.refresh_from_db()
            self.assertFalse(travel_picture.travel_picture)
            self.assertEqual(f'Max file size is {TravelPicture.MAX_IMAGE_SIZE_IN_MB}.00 MB',
                             response.context_data['form'].errors['travel_picture'][0])

    def test_invalid_file_content_type(self):
        visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        cities = VisitedCity.objects.filter(user=self.user).all()
        travel_picture = TravelPicture.objects.create(
            # travel_picture=self.travel_picture,
            title=self.title,
            located_city=visited_city,
            user=self.user,
        )
        with open(os.path.join(BASE_DIR,
                               'staticfiles',
                               'default_files',
                               'invalid_test_file.txt'), 'rb') as invalid_picture:
            data = {
                'title': self.title,
                'travel_picture': SimpleUploadedFile(
                    name='invalid_test_file.txt',
                    content=invalid_picture.read(),
                    content_type='plain/txt',
                ),
                'located_city': visited_city.pk,
            }
            response = self.client.post(reverse('travel picture edit',
                                                kwargs={'pk': travel_picture.pk}),
                                        data=data,
                                        located_city=cities,
                                        user=self.user)
            self.assertEqual(f'Please select an image file!',
                             response.context_data['form'].errors['travel_picture'][0])
