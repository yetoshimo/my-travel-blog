from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class MyTravelBlogUserManager(BaseUserManager):
    TERMINAL_USER_FIRST_NAME = 'Terminal First'
    TERMINAL_USER_LAST_NAME = 'Terminal Last'
    TERMINAL_USER_PROFILE_PICTURE = 'Terminal Picture'

    def _create_user(self, email, password, **extra_fields):

        from mytravelblog.accounts.models import Profile
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        profile = Profile(
            first_name=self.TERMINAL_USER_FIRST_NAME,
            last_name=self.TERMINAL_USER_LAST_NAME,
            profile_picture=self.TERMINAL_USER_PROFILE_PICTURE,
            user=user,
        )
        profile.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
