from django import test as django_tests

from mytravelblog.main_app.forms.travel_picture import *
from mytravelblog.main_app.models import *

UserModel = get_user_model()


class TravelPictureRegistrationFormTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword2'
        self.city_name = 'sofia'
        self.country_name = 'bulgaria'
        self.travel_picture = 'test-picture.jpg'
        self.title = 'Picture Lorem Ipsum'
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

    def test_travel_picture_form_correctly_saves_with_valid_data(self):
        data = {
            'travel_picture': self.travel_picture,
            'title': self.title,
            'located_city': self.located_city,
        }

        travel_picture_form = TravelPictureRegistrationForm(user=self.user, data=data, located_city=self.cities)
        self.assertTrue(travel_picture_form.is_valid())
        travel_picture_form.save()
        self.assertEqual(self.user, travel_picture_form.user)
        self.assertEqual(self.title, travel_picture_form.cleaned_data['title'])
        self.assertEqual(self.located_city, travel_picture_form.cleaned_data['located_city'])
        self.assertEqual(1, TravelPicture.objects.count())

    def test_travel_picture_form_cannot_save_duplicate_name(self):
        travel_picture = TravelPicture.objects.create(
            travel_picture=self.travel_picture,
            title=self.title,
            located_city=self.located_city,
            user=self.user,
        )
        self.assertEqual(1, TravelPicture.objects.count())

        data = {
            'travel_picture': self.travel_picture,
            'title': self.title,
            'located_city': self.located_city,
        }
        travel_picture_form = TravelPictureRegistrationForm(user=self.user, data=data, located_city=self.cities)
        self.assertFalse(travel_picture_form.is_valid())
        self.assertEqual(f'Picture with title "{self.title}" already exists!',
                         travel_picture_form.errors['title'][0])
