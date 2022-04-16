import asyncio

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

    async def get_travel_entries(self):
        return TravelEntry.objects.filter(user=self.request.user).all()

    async def get_travel_pictures(self):
        return TravelEntry.objects.filter(user=self.request.user).all()

    async def get_visited_cities(self):
        return VisitedCity.objects.filter(user=self.request.user).all()

    async def get_visited_hotels(self):
        return VisitedHotel.objects.filter(user=self.request.user).all()

    async def get_user_related_data(self):
        return await asyncio.gather(
            self.get_travel_entries(),
            self.get_travel_pictures(),
            self.get_visited_cities(),
            self.get_visited_hotels()
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['travel_entries'], context['cities'], context['hotels'], context['travel_pictures'] = asyncio.run(
            self.get_user_related_data())
        return context
