from django import test as django_tests

from mytravelblog.main_app.forms.travel_picture import *
from mytravelblog.main_app.models import *

UserModel = get_user_model()


class TravelPictureEditFormTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword2'
        self.city_name = 'sofia'
        self.country_name = 'bulgaria'
        self.travel_picture = 'test-picture.jpg'
        self.travel_picture_update = 'test-picture-two.jpg'
        self.title = 'Picture Lorem Ipsum'
        self.title_two = 'Picture Two Lorem Ipsum'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.located_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )

        self.cities = VisitedCity.objects.filter(user=self.user).all()

    def test_travel_picture_edit_form_saves_with_valid_data(self):
        travel_picture = TravelPicture.objects.create(
            # travel_picture=self.travel_picture,
            title=self.title,
            located_city=self.located_city,
            user=self.user,
        )
        self.assertEqual(1, TravelPicture.objects.count())

        data = {
            # 'travel_picture': self.travel_picture_update,
            'title': self.title_two,
            'located_city': self.located_city,
        }

        travel_picture_edit_form = TravelPictureEditForm(instance=travel_picture, data=data, located_city=self.cities)
        self.assertTrue(travel_picture_edit_form.is_valid())
        travel_picture_edit_form.save()
        self.assertEqual(self.title_two, travel_picture.title)


    def test_travel_picture_edit_form_cannot_save_duplicate_picture_with_same_title(self):
        travel_picture_one = TravelPicture.objects.create(
            # travel_picture=self.travel_picture,
            title=self.title,
            located_city=self.located_city,
            user=self.user,
        )
        travel_picture_two = TravelPicture.objects.create(
            # travel_picture=self.travel_picture_update,
            title=self.title_two,
            located_city=self.located_city,
            user=self.user,
        )
        self.assertNotEqual(travel_picture_one.title, travel_picture_two.title)
        data = {
            # 'travel_picture': self.travel_picture,
            'title': self.title,
            'located_city': self.located_city,
        }
        travel_picture_edit_form = TravelPictureEditForm(instance=travel_picture_two, data=data,
                                                         located_city=self.cities)
        self.assertFalse(travel_picture_edit_form.is_valid())
        self.assertEqual('Travel Picture with this Title already exists.',
                         travel_picture_edit_form.errors['title'][0])
