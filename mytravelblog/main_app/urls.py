from django.urls import path

from mytravelblog.main_app.views.city import *
from mytravelblog.main_app.views.hotel import *
from mytravelblog.main_app.views.generic import *
from mytravelblog.main_app.views.picture import *
from mytravelblog.main_app.views.travel_entry import *

urlpatterns = (
    path('', HomeView.as_view(), name='show home'),
    path('dashboard/', DashboardView.as_view(), name='show dashboard'),
    path('show-cities/', VisitedCitiesView.as_view(), name='cities view'),
    path('show-hotels/', VisitedHotelsView.as_view(), name='hotels view'),
    path('show-travel-pictures/', TravelPicturesView.as_view(), name='travel pictures view'),
    path('travel-entry-view/<int:pk>', TravelEntryDetailsView.as_view(), name='travel entry details'),

    path('register-city/', CityRegisterView.as_view(), name='register city'),
    path('edit-city/<int:pk>/', EditVisitedCityView.as_view(), name='city edit'),
    path('delete-city/<int:pk>/', DeleteVisitedCityView.as_view(), name='city delete'),

    path('register-hotel/', HotelRegisterView.as_view(), name='register hotel'),
    path('edit-hotel/<int:pk>/', EditVisitedHotelView.as_view(), name='hotel edit'),
    path('delete-hotel/<int:pk>/', DeleteVisitedHotelView.as_view(), name='hotel delete'),

    path('register-travel-picture/', TravelPictureRegisterView.as_view(), name='register travel picture'),
    path('edit-travel-picture/<int:pk>/', EditTravelPictureView.as_view(), name='travel picture edit'),
    path('delete-travel-picture/<int:pk>/', DeleteTravelPictureView.as_view(), name='travel picture delete'),

    path('register-travel-entry/', TravelEntryRegisterView.as_view(), name='register travel entry'),
    path('edit-travel-entry/<int:pk>/', EditTravelEntryView.as_view(), name='travel entry edit'),
    path('delete-travel-entry/<int:pk>/', DeleteTravelEntryView.as_view(), name='travel entry delete'),
)
