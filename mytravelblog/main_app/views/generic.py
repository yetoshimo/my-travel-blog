from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from django.views import generic as generic_views

from mytravelblog.main_app.models import *


class HomeView(generic_views.TemplateView):
    template_name = 'main_app/generic/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('show dashboard')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, generic_views.ListView):
    model = TravelEntry
    template_name = 'main_app/generic/dashboard.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['travel_entries'] = TravelEntry.objects.filter(user=self.request.user).all()
        context['cities'] = VisitedCity.objects.filter(user=self.request.user).all()
        context['hotels'] = VisitedHotel.objects.filter(user=self.request.user).all()
        context['travel_pictures'] = TravelPicture.objects.filter(user=self.request.user).all()
        return context
