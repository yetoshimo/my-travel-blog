from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.contrib.auth import models as auth_models

from mytravelblog.accounts.managers import MyTravelBlogUserManager
from mytravelblog.accounts.validators import *


class MyTravelBlogUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    COUNTRIES_MAX_LENGTH = 50
    COUNTRIES_MIN_LENGTH = 4
    EMAIL_MAX_LENGTH = 254

    email = models.EmailField(
        unique=True,
        validators=(
            MaxLengthValidator(EMAIL_MAX_LENGTH),
        ),
    )

    current_country = models.CharField(
        max_length=COUNTRIES_MAX_LENGTH,
        validators=(
            MinLengthValidator(COUNTRIES_MIN_LENGTH),
        ),
        verbose_name='Current Country',
    )

    account_creation_date = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['current_country', ]

    @property
    def get_email_username(self):
        return self.email.split("@")[0]

    def save(self, *args, **kwargs):
        self.current_country = self.current_country.title()
        super().save(*args, **kwargs)

    objects = MyTravelBlogUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        ordering = ('id',)


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 32
    FIRST_NAME_MIN_LENGTH = 2

    LAST_NAME_MAX_LENGTH = 32
    LAST_NAME_MIN_LENGTH = 2

    URL_FIELD_MAX_LENGTH = 200

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            RegexValidator(regex='^([a-zA-Z]+)$',
                           message='Ensure this value contains only letters.',
                           code='Invalid first name'),
        ),
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            RegexValidator(regex='^([a-zA-Z]+)$',
                           message='Ensure this value contains only letters.',
                           code='Invalid last name'),
        ),
    )

    profile_picture = models.URLField(
        validators=(
            MaxLengthValidator(URL_FIELD_MAX_LENGTH),
        ),
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name='Date of Birth',
    )

    user = models.OneToOneField(
        MyTravelBlogUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
