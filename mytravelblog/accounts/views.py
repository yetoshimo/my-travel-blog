import cloudinary.uploader
from django.contrib.auth import views as auth_views, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as generic_views

from mytravelblog.accounts.forms import *

UserModel = get_user_model()


class UserRegisterView(generic_views.CreateView):
    template_name = 'accounts/profile/profile_create.html'
    success_url = reverse_lazy('show dashboard')
    form_class = CreateProfileForm

    def form_valid(self, form, *args, **kwargs):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('show dashboard')
    form_class = UserLoginForm

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserLogoutConfirmationView(LoginRequiredMixin, generic_views.TemplateView):
    template_name = 'accounts/logout_page.html'


class UserLogoutView(LoginRequiredMixin, auth_views.LogoutView):

    def get_next_page(self):
        return reverse_lazy('show home')


class UserProfileDetailsView(LoginRequiredMixin, generic_views.DetailView):
    model = Profile
    template_name = 'accounts/profile/profile_details.html'
    context_object_name = 'profile'

    def dispatch(self, request, *args, **kwargs):
        if Profile.objects.filter(user_id=kwargs['pk']).exists() and \
                request.user == Profile.objects.get(user_id=kwargs['pk']).user:
            return super().dispatch(request, *args, **kwargs)
        return redirect('profile details', self.request.user.id)


class EditProfileView(LoginRequiredMixin, generic_views.UpdateView):
    model = Profile
    template_name = 'accounts/profile/profile_edit.html'
    form_class = EditProfileForm
    context_object_name = 'profile'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object.user
        return kwargs

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile details', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form, *args, **kwargs):
        if 'profile_picture' in form.changed_data:
            if form.cleaned_data['profile_picture'] and self.request.user.profile.profile_picture:
                cloudinary.uploader.destroy(self.request.user.profile.profile_picture.public_id, invalidate=True, )
            elif not form.cleaned_data['profile_picture']:
                cloudinary.uploader.destroy(self.request.user.profile.profile_picture.public_id, invalidate=True, )
        result = super().form_valid(form)
        user = self.object.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()
        return result


class DeleteProfileView(LoginRequiredMixin, generic_views.DeleteView):
    model = UserModel
    template_name = 'accounts/profile/delete_profile_page.html'
    success_url = reverse_lazy('show home')


class ChangeUserPasswordView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = EditPasswordForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile details', kwargs={'pk': self.request.user.pk})
