import cloudinary.uploader
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
        if request.user.is_authenticated:
            result = VisitedCity.objects.filter(user=self.request.user).exists()
            if result:
                return super().dispatch(request, *args, **kwargs)
            return redirect('register city')
        return super().dispatch(request, *args, **kwargs)


class TravelPicturesView(LoginRequiredMixin, generic_views.ListView):
    model = TravelPicture
    template_name = 'main_app/generic/travel_pictures.html'
    context_object_name = 'travel_pictures'
    ordering = ('located_city', '-uploaded_on',)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).all()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            result = super().get_queryset().filter(user=self.request.user).exists()
            if result:
                return super().dispatch(request, *args, **kwargs)
            return redirect('show dashboard')
        return super().dispatch(request, *args, **kwargs)


class EditTravelPictureView(LoginRequiredMixin, generic_views.UpdateView):
    model = TravelPicture
    template_name = 'main_app/travel_picture/edit_travel_picture.html'
    success_url = reverse_lazy('travel pictures view')
    form_class = TravelPictureEditForm
    context_object_name = 'travel_picture'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['located_city'] = VisitedCity.objects.filter(user=self.request.user).all()
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        if 'travel_picture' in form.changed_data:
            # GET THE EXISTING OBJECT ( NOT IN-MEMORY )
            tp_to_update = TravelPicture.objects.get(pk=self.object.pk)
            if form.cleaned_data['travel_picture'] and tp_to_update.travel_picture:
                # IF UPDATED REMOVE THE EXISTING ONE
                cloudinary.uploader.destroy(tp_to_update.travel_picture.public_id,
                                            invalidate=True, )
            elif not self.object.travel_picture:
                # IF CLEARED REMOVE THE EXISTING ONE
                cloudinary.uploader.destroy(tp_to_update.travel_picture.public_id,
                                            invalidate=True, )
        result = super().form_valid(form)
        return result

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            result = super().get_queryset().filter(user=self.request.user, pk=kwargs['pk']).exists()
            if result:
                return super().dispatch(request, *args, **kwargs)
            return redirect('travel pictures view')
        return super().dispatch(request, *args, **kwargs)


class DeleteTravelPictureView(LoginRequiredMixin, generic_views.DeleteView):
    model = TravelPicture
    template_name = 'main_app/travel_picture/delete_travel_picture.html'
    success_url = reverse_lazy('travel pictures view')
    form_class = TravelPictureDeleteForm
    context_object_name = 'travel_picture'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            result = super().get_queryset().filter(user=self.request.user, pk=kwargs['pk']).exists()
            if result:
                return super().dispatch(request, *args, **kwargs)
            return redirect('travel pictures view')
        return super().dispatch(request, *args, **kwargs)
