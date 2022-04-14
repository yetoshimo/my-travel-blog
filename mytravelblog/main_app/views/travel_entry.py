from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as generic_views

from mytravelblog.main_app.forms.travel_entry import *
from mytravelblog.main_app.models import *


class TravelEntryRegisterView(LoginRequiredMixin, generic_views.CreateView):
    model = TravelEntry
    template_name = 'main_app/travel_entry/travel_entry.create.html'
    success_url = reverse_lazy('show dashboard')
    form_class = TravelEntryRegistrationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['visited_city'] = VisitedCity.objects.filter(user=self.request.user).all()
        kwargs['visited_hotel'] = VisitedHotel.objects.filter(user=self.request.user).all()
        kwargs['travel_picture'] = TravelPicture.objects.filter(user=self.request.user).all()
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        result = VisitedCity.objects.filter(user=self.request.user).all()
        if result:
            return super().dispatch(request, *args, **kwargs)
        return redirect('register city')


class TravelEntryDetailsView(LoginRequiredMixin, generic_views.DetailView):
    model = TravelEntry
    template_name = 'main_app/travel_entry/travel_entry.details.html'
    context_object_name = 'travel_entry'
    ordering = ('-publish_date_time',)


class EditTravelEntryView(LoginRequiredMixin, generic_views.UpdateView):
    model = TravelEntry
    template_name = 'main_app/travel_entry/edit_travel_entry.html'
    form_class = TravelEntryEditForm
    context_object_name = 'travel_entry'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['visited_city'] = VisitedCity.objects.filter(user=self.request.user).all()
        kwargs['visited_hotel'] = VisitedHotel.objects.filter(user=self.request.user).all()
        kwargs['travel_picture'] = TravelPicture.objects.filter(user=self.request.user).all()
        return kwargs

    def get_success_url(self):
        return reverse_lazy('travel entry details', kwargs={'pk': self.object.id})


class DeleteTravelEntryView(LoginRequiredMixin, generic_views.DeleteView):
    model = TravelEntry
    template_name = 'main_app/travel_entry/delete_travel_entry.html'
    success_url = reverse_lazy('show dashboard')
    form_class = TravelEntryDeleteForm
    context_object_name = 'travel_entry'
