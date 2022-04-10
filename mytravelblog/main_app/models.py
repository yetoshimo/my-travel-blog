from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

UserModel = get_user_model()


class VisitedCity(models.Model):
    CITY_NAME_MAX_LENGTH = 64

    COUNTRY_NAME_MAX_LENGTH = 50
    COUNTRIES_MIN_LENGTH = 4

    city_name = models.CharField(
        max_length=CITY_NAME_MAX_LENGTH,
        verbose_name='City Name',
    )

    country_name = models.CharField(
        max_length=COUNTRY_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(COUNTRIES_MIN_LENGTH),
        ),
        verbose_name='Country Name',
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.city_name}, {self.country_name}'

    def save(self, *args, **kwargs):
        self.city_name = self.city_name.title()
        self.country_name = self.country_name.title()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

        unique_together = (
            'city_name',
            'country_name',
        )

        ordering = ('city_name', 'country_name',)


class VisitedHotel(models.Model):
    HOTEL_NAME_MAX_LENGTH = 64

    NUMBER_OF_STARTS = [(s, s) for s in ('1', '2', '3', '4', '5')]

    hotel_name = models.CharField(
        max_length=HOTEL_NAME_MAX_LENGTH,
        verbose_name='Hotel Name',
    )

    number_of_stars = models.CharField(
        max_length=1,
        choices=NUMBER_OF_STARTS,
        verbose_name='Number of Stars',
    )

    star_count = models.CharField(
        max_length=20,
        verbose_name='Star Count',
    )

    located_city = models.ForeignKey(
        VisitedCity,
        on_delete=models.CASCADE,
        verbose_name='Located City',
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.hotel_name}, {self.located_city}'

    def save(self, *args, **kwargs):
        self.star_count = ''.join([str(i) for i in range(int(self.number_of_stars))])
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'

        unique_together = (
            'located_city',
            'hotel_name',
        )

        ordering = ('hotel_name', 'located_city',)


class TravelPicture(models.Model):
    URL_FIELD_MAX_LENGTH = 200
    TITLE_MAX_LENGTH = 64

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        unique=True,
    )

    travel_picture = models.URLField(
        validators=(
            MaxLengthValidator(URL_FIELD_MAX_LENGTH),
        ),
        null=True,
        blank=True,
    )

    located_city = models.ForeignKey(
        VisitedCity,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    uploaded_on = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.title}, {self.located_city}'

    class Meta:
        verbose_name = 'Travel Picture'
        verbose_name_plural = 'Travel Pictures'


class TravelEntry(models.Model):
    TITLE_MAX_LENGTH = 32

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name='Entry Title',
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    publish_date_time = models.DateTimeField(
        auto_now_add=True,
    )

    visited_city = models.ForeignKey(
        VisitedCity,
        on_delete=models.CASCADE,
    )

    visited_hotel = models.ForeignKey(
        VisitedHotel,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    travel_picture = models.ForeignKey(
        TravelPicture,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title}, {self.visited_city}'

    class Meta:
        verbose_name = 'Travel Entry'
        verbose_name_plural = 'Travel Entries'
