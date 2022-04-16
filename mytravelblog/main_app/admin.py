from django.contrib import admin

from mytravelblog.main_app.models import *


@admin.register(VisitedCity)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'country_name', 'user',)
    list_filter = ('user',)
    search_fields = ('city_name',)
    list_display_links = ('city_name', 'country_name',)
    fields = (
        'user',
        'city_name',
        'country_name',
    )


@admin.register(VisitedHotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_name', 'located_city', 'user',)
    list_filter = ('user',)
    search_fields = ('hotel_name',)
    list_display_links = ('hotel_name', 'located_city',)
    fields = (
        'user',
        'hotel_name',
        'located_city',
    )


@admin.register(TravelPicture)
class TravelPictureAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'travel_picture',
        'located_city',
        'uploaded_on',
        'user',
    )
    list_filter = ('user',)
    search_fields = ('title',)
    list_display_links = ('title',)


@admin.register(TravelEntry)
class TravelEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'visited_city', 'user',)
    list_filter = ('user',)
    search_fields = ('title',)
    list_display_links = ('title',)
