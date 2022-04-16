import os.path

from http import HTTPStatus

from django import test as django_tests
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

import cloudinary.uploader

from mytravelblog.accounts.models import Profile
from mytravelblog.settings import BASE_DIR

UserModel = get_user_model()


class EditProfileViewTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.first_name = 'testuser-firstname'
        self.last_name = 'testuser-lastname'
        self.email = 'testuser@email.com'
        self.current_country = 'Bulgaria'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )

        self.client.login(username=self.username, password=self.password1)

    def test_edit_profile_view_url(self):
        response = self.client.get(f'/accounts/edit-profile/{self.user.id}/')
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, template_name='accounts/profile/profile_edit.html')

    def test_edit_profile_view_name(self):
        response = self.client.get(reverse('profile edit', kwargs={'pk': self.user.id}))
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(self.user, response.context['user'])
        self.assertTemplateUsed(response, template_name='accounts/profile/profile_edit.html')

    def test_edit_profile_view_successful_redirect(self):
        response = self.client.post(reverse('profile edit', kwargs={'pk': self.user.id}))
        self.assertEqual(HTTPStatus.FOUND, response.status_code)
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': self.user.id}))

    def test_edit_profile_upload_picture(self):
        p = Profile.objects.get(user=self.user)
        self.assertFalse(p.profile_picture)
        with open(os.path.join(BASE_DIR,
                               'staticfiles',
                               'default_files',
                               'default_profile_picture.png'), 'rb') as cloudinary_profile_picture:
            data = {
                'profile_picture': SimpleUploadedFile(
                    name='default_profile_picture.png',
                    content=cloudinary_profile_picture.read(),
                    content_type='image/png',
                ),
            }
            response = self.client.post(reverse('profile edit', kwargs={'pk': self.user.id}), data=data, user=self.user)
            p.refresh_from_db()
            self.assertTrue(p.profile_picture)
            cloudinary.uploader.destroy(p.profile_picture.public_id, invalidate=True, )

    def test_edit_profile_update_existing_profile_picture(self):
        p = Profile.objects.get(user=self.user)
        self.assertFalse(self.user.profile.profile_picture)
        with open(os.path.join(BASE_DIR,
                               'staticfiles',
                               'default_files',
                               'default_profile_picture.png'), 'rb') as cloudinary_profile_picture:
            data = {
                'profile_picture': SimpleUploadedFile(
                    name='default_profile_picture.png',
                    content=cloudinary_profile_picture.read(),
                    content_type='image/png',
                ),
            }
            self.client.post(reverse('profile edit', kwargs={'pk': self.user.id}), data=data, user=self.user)
            p.refresh_from_db()
            old_public_id = p.profile_picture.public_id
            with open(os.path.join(BASE_DIR,
                                   'staticfiles',
                                   'default_files',
                                   'default_world_picture.png'), 'rb') as cloudinary_profile_picture2:
                data2 = {
                    'profile_picture': SimpleUploadedFile(
                        name='default_world_picture.png',
                        content=cloudinary_profile_picture2.read(),
                        content_type='image/png',
                    ),
                }
                response = self.client.post(reverse('profile edit', kwargs={'pk': self.user.id}), data=data2,
                                            user=self.user)
                p.refresh_from_db()
                new_public_id = p.profile_picture.public_id
                self.assertNotEqual(old_public_id, new_public_id)
                cloudinary.uploader.destroy(old_public_id, invalidate=True, )
                cloudinary.uploader.destroy(new_public_id, invalidate=True, )

    def test_edit_profile_picture_clear_existing_profile_picture(self):
        p = Profile.objects.get(user=self.user)
        self.assertFalse(self.user.profile.profile_picture)
        with open(os.path.join(BASE_DIR,
                               'staticfiles',
                               'default_files',
                               'default_profile_picture.png'), 'rb') as cloudinary_profile_picture:
            data = {
                'profile_picture': SimpleUploadedFile(
                    name='default_profile_picture.png',
                    content=cloudinary_profile_picture.read(),
                    content_type='image/png',
                ),
            }
            self.client.post(reverse('profile edit', kwargs={'pk': self.user.id}), data=data, user=self.user)
            p.refresh_from_db()
            old_public_id = p.profile_picture.public_id
            data2 = {
                'profile_picture-clear': 'on',
            }
            response = self.client.post(reverse('profile edit', kwargs={'pk': self.user.id}), data=data2,
                                        user=self.user)
            p.refresh_from_db()
            self.assertFalse(p.profile_picture)
            cloudinary.uploader.destroy(old_public_id, invalidate=True, )

    def test_edit_profile_picture_error_on_too_big_file(self):
        p = Profile.objects.get(user=self.user)
        self.assertFalse(p.profile_picture)
        with open(os.path.join(BASE_DIR,
                               'staticfiles',
                               'default_files',
                               'default_big_file.JPG'), 'rb') as cloudinary_profile_picture:
            data = {
                'profile_picture': SimpleUploadedFile(
                    name='default_big_file.JPG',
                    content=cloudinary_profile_picture.read(),
                    content_type='image/png',
                ),
            }
            response = self.client.post(reverse('profile edit', kwargs={'pk': self.user.id}), data=data, user=self.user)
            p.refresh_from_db()
            self.assertFalse(p.profile_picture)
            self.assertEqual(f'Max file size is {Profile.MAX_IMAGE_SIZE_IN_MB}.00 MB',
                             response.context_data['form'].errors['profile_picture'][0])

    def test_invalid_file_content_type(self):
        with open(os.path.join(BASE_DIR,
                               'staticfiles',
                               'default_files',
                               'invalid_test_file.txt'), 'rb') as invalid_picture:
            data = {
                'profile_picture': SimpleUploadedFile(
                    name='invalid_test_file.txt',
                    content=invalid_picture.read(),
                    content_type='text/plain',
                ),
            }
            response = self.client.post(reverse('profile edit', kwargs={'pk': self.user.id}), data=data, user=self.user)
            self.assertEqual(f'Please select an image file!',
                             response.context_data['form'].errors['profile_picture'][0])
