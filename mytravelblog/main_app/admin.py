from django.contrib import admin

from mytravelblog.main_app.models import *


@admin.register(VisitedCity)
class CityAdmin(admin.ModelAdmin):
    list_display = ('user', 'city_name', 'country_name',)
    list_filter = ('user', 'country_name', 'city_name',)

    fields = (
        'user',
        'city_name',
        'country_name',
    )


@admin.register(VisitedHotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel_name', 'located_city',)
    list_filter = ('user', 'number_of_stars', 'located_city',)

    fields = (
        'user',
        'hotel_name',
        'located_city',
    )


@admin.register(TravelPicture)
class TravelPictureAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'title',
        'travel_picture',
        'located_city',
        'uploaded_on',
    )

    list_filter = (
        'user',
        'located_city',
    )


@admin.register(TravelEntry)
class TravelEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'visited_city',)
    list_filter = ('user', 'visited_city',)
