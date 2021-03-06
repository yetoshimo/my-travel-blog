from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as generic_views

from mytravelblog.main_app.forms.city import *
from mytravelblog.main_app.models import *


class CityRegisterView(LoginRequiredMixin, generic_views.CreateView):
    model = VisitedCity
    template_name = 'main_app/city/city_create.html'
    success_url = reverse_lazy('cities view')
    form_class = CityRegistrationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_cities'] = VisitedCity.objects.filter(user=self.request.user).exists()
        return context


class VisitedCitiesView(LoginRequiredMixin, generic_views.ListView):
    model = VisitedCity
    template_name = 'main_app/generic/visited_cities.html'
    context_object_name = 'cities'
    ordering = ('city_name', 'country_name',)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).all()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            result = super().get_queryset().filter(user=self.request.user).exists()
            if result:
                return super().dispatch(request, *args, **kwargs)
            return redirect('show dashboard')
        return super().dispatch(request, *args, **kwargs)


class EditVisitedCityView(LoginRequiredMixin, generic_views.UpdateView):
    model = VisitedCity
    template_name = 'main_app/city/edit_city.html'
    success_url = reverse_lazy('cities view')
    form_class = CityEditForm
    context_object_name = 'city'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).all()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            result = super().get_queryset().filter(user=self.request.user, pk=kwargs['pk']).exists()
            if result:
                return super().dispatch(request, *args, **kwargs)
            return redirect('cities view')
        return super().dispatch(request, *args, **kwargs)


class DeleteVisitedCityView(LoginRequiredMixin, generic_views.DeleteView):
    model = VisitedCity
    template_name = 'main_app/city/delete_city.html'
    success_url = reverse_lazy('cities view')
    form_class = CityDeleteForm
    context_object_name = 'city'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            result = super().get_queryset().filter(user=self.request.user, pk=kwargs['pk']).exists()
            if result:
                return super().dispatch(request, *args, **kwargs)
            return redirect('cities view')
        return super().dispatch(request, *args, **kwargs)
