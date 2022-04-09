from django.contrib import admin

# Register your models here.
from mytravelblog.main_app.models import *


@admin.register(VisitedCity)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(VisitedHotel)
class HotelAdmin(admin.ModelAdmin):
    pass


@admin.register(TravelPicture)
class TravelPictureAdmin(admin.ModelAdmin):
    pass


@admin.register(TravelEntry)
class TravelEntryAdmin(admin.ModelAdmin):
    pass
