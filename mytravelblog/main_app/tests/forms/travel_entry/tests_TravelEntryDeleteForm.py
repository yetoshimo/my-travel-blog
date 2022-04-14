from django import test as django_tests

from mytravelblog.main_app.forms.travel_entry import *
from mytravelblog.main_app.models import *

UserModel = get_user_model()


class TravelEntryDeleteFormTests(django_tests.TestCase):
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

    def test_travel_entry_delete_form_initiates_successfully(self):
        travel_entry = TravelEntry.objects.create(
            title=self.travel_entry_title,
            description=self.description,
            user=self.user,
            visited_city=self.visited_city,
            visited_hotel=self.visited_hotel,
            # travel_picture=self.travel_picture,
        )
        self.assertEqual(1, TravelEntry.objects.count())
        TravelEntryDeleteForm(instance=travel_entry)
