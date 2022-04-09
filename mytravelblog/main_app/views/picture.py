from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as generic_views

from mytravelblog.main_app.forms.travel_picture import *
from mytravelblog.main_app.models import *


class TravelPictureRegisterView(LoginRequiredMixin, generic_views.CreateView):
    model = TravelPicture
    template_name = 'main_app/travel_picture/travel_picture_create.html'
    success_url = reverse_lazy('travel pictures view')
    form_class = TravelPictureRegistrationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['located_city'] = VisitedCity.objects.filter(user=self.request.user).all()
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        result = VisitedCity.objects.filter(user=self.request.user).all()
        if result:
            return super().dispatch(request, *args, **kwargs)
        return redirect('show dashboard')


class TravelPicturesView(LoginRequiredMixin, generic_views.ListView):
    model = TravelPicture
    template_name = 'main_app/generic/travel_pictures.html'
    context_object_name = 'travel_pictures'
    ordering = ('located_city', 'uploaded_on',)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).all()

    def dispatch(self, request, *args, **kwargs):
        result = super().get_queryset().filter(user=self.request.user).all()
        if result:
            return super().dispatch(request, *args, **kwargs)
        return redirect('show dashboard')


class EditTravelPictureView(LoginRequiredMixin, generic_views.UpdateView):
    model = TravelPicture
    template_name = 'main_app/travel_picture/edit_travel_picture.html'
    success_url = reverse_lazy('travel pictures view')
    form_class = TravelPictureEditForm
    context_object_name = 'travel_picture'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['located_city'] = VisitedCity.objects.filter(user=self.request.user).all()
        return kwargs


class DeleteTravelPictureView(LoginRequiredMixin, generic_views.DeleteView):
    model = TravelPicture
    template_name = 'main_app/travel_picture/delete_travel_picture.html'
    success_url = reverse_lazy('travel pictures view')
    form_class = TravelPictureDeleteForm
    context_object_name = 'travel_picture'
