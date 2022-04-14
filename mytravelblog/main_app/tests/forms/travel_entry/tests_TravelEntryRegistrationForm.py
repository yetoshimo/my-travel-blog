from django import test as django_tests

from mytravelblog.main_app.forms.travel_entry import *
from mytravelblog.main_app.models import *

UserModel = get_user_model()


class TravelEntryRegistrationFormTests(django_tests.TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password1 = 'P@ssword1'
        self.password2 = 'P@ssword2'
        self.city_name = 'sofia'
        self.country_name = 'bulgaria'
        self.hotel_name = 'Grand Hotel Sofia'
        self.number_of_stars = '4'
        self.star_count = ''.join([str(i) for i in range(int(self.number_of_stars))])
        self.travel_entry_title = 'Lorem Ipsum'
        self.description = 'Lorem ipsum dolor sit amet.'
        self.travel_picture = 'test-picture.jpg'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password1,
        )
        self.visited_city = VisitedCity.objects.create(
            city_name=self.city_name,
            country_name=self.country_name,
            user=self.user,
        )
        self.visited_hotel = VisitedHotel.objects.create(
            hotel_name=self.hotel_name,
            located_city=self.visited_city,
            number_of_stars=self.number_of_stars,
            user=self.user,
            star_count=self.star_count,
        )

        self.cities = VisitedCity.objects.filter(user=self.user).all()
        self.hotels = VisitedHotel.objects.filter(user=self.user).all()
        self.travel_pictures = TravelPicture.objects.filter(user=self.user).all()

    def test_travel_entry_form_saves_with_valid_data(self):
        data = {
            'title': self.travel_entry_title,
            'description': self.description,
            'visited_city': self.visited_city,
            'visited_hotel': self.visited_hotel,
            # 'travel_picture': self.travel_picture,
        }

        travel_entry_form = TravelEntryRegistrationForm(data=data,
                                                        user=self.user,
                                                        visited_city=self.cities,
                                                        visited_hotel=self.hotels,
                                                        travel_picture=self.travel_pictures,
                                                        )
        self.assertTrue(travel_entry_form.is_valid())
        travel_entry_form.save()
        self.assertEqual(self.user, travel_entry_form.user)
        self.assertEqual(self.travel_entry_title, travel_entry_form.cleaned_data['title'])
        self.assertEqual(self.description, travel_entry_form.cleaned_data['description'])
        self.assertEqual(self.visited_city, travel_entry_form.cleaned_data['visited_city'])
        self.assertEqual(self.visited_hotel, travel_entry_form.cleaned_data['visited_hotel'])
