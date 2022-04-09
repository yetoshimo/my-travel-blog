from django.urls import path

from mytravelblog.accounts.views import *

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutConfirmationView.as_view(), name='logout user confirmation'),
    path('logout/signout/', UserLogoutView.as_view(), name='logout user'),

    path('profile_details/<int:pk>/', UserProfileDetailsView.as_view(), name='profile details'),
    path('profile/create/', UserRegisterView.as_view(), name='profile create'),
    path('edit-profile/<int:pk>/', EditProfileView.as_view(), name='profile edit'),
    path('delete-profile/<int:pk>/', DeleteProfileView.as_view(), name='profile delete'),

    path('edit-password/<int:pk>/', ChangeUserPasswordView.as_view(), name='change password'),
)
