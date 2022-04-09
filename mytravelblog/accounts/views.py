from django.contrib.auth import views as auth_views, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic as generic_views

from mytravelblog.accounts.forms import *


class UserRegisterView(generic_views.CreateView):
    template_name = 'accounts/profile/profile_create.html'
    success_url = reverse_lazy('show dashboard')
    form_class = CreateProfileForm

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
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


class EditProfileView(LoginRequiredMixin, generic_views.UpdateView):
    model = Profile
    template_name = 'accounts/profile/profile_edit.html'
    form_class = EditProfileForm
    context_object_name = 'profile'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['email'] = self.object.user.email
        kwargs['current_country'] = self.object.user.current_country
        return kwargs

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile details', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form, *args, **kwargs):
        result = super().form_valid(form)
        user = self.object.user
        user.email = form.cleaned_data['email']
        user.current_country = form.cleaned_data['current_country']
        user.save()
        return result


class DeleteProfileView(LoginRequiredMixin, generic_views.DeleteView):
    model = Profile
    template_name = 'accounts/profile/delete_profile_page.html'
    success_url = reverse_lazy('show home')

    def form_valid(self, form, *args, **kwargs):
        user = self.object.user
        user.delete()
        result = super().form_valid(form)
        return result


class ChangeUserPasswordView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = EditPasswordForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile details', kwargs={'pk': self.request.user.pk})
