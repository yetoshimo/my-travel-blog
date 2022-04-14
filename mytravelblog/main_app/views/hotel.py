from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as generic_views

from mytravelblog.main_app.forms.hotel import *
from mytravelblog.main_app.models import *


class HotelRegisterView(LoginRequiredMixin, generic_views.CreateView):
    model = VisitedHotel
    template_name = 'main_app/hotel/hotel_create.html'
    success_url = reverse_lazy('hotels view')
    form_class = HotelRegistrationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['located_city'] = VisitedCity.objects.filter(user=self.request.user).all()
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        result = VisitedCity.objects.filter(user=self.request.user).all()
        if result:
            return super().dispatch(request, *args, **kwargs)
        return redirect('register city')


class VisitedHotelsView(LoginRequiredMixin, generic_views.ListView):
    model = VisitedHotel
    template_name = 'main_app/generic/visited_hotels.html'
    context_object_name = 'hotels'
    ordering = ('number_of_stars', 'hotel_name',)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).all()

    def dispatch(self, request, *args, **kwargs):
        result = super().get_queryset().filter(user=self.request.user).all()
        if result:
            return super().dispatch(request, *args, **kwargs)
        return redirect('show dashboard')


class EditVisitedHotelView(LoginRequiredMixin, generic_views.UpdateView):
    model = VisitedHotel
    template_name = 'main_app/hotel/edit_hotel.html'
    success_url = reverse_lazy('hotels view')
    form_class = HotelEditForm
    context_object_name = 'hotel'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['located_city'] = VisitedCity.objects.filter(user=self.request.user).all()
        return kwargs


class DeleteVisitedHotelView(LoginRequiredMixin, generic_views.DeleteView):
    model = VisitedHotel
    template_name = 'main_app/hotel/delete_hotel.html'
    success_url = reverse_lazy('hotels view')
    form_class = HotelDeleteForm
    context_object_name = 'hotel'
