import cloudinary.uploader
from cloudinary import models as cloudinary_models
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver

from mytravelblog.common.validators import ImageSizeInMBValidator

"""
Ways to extend the User model
Having its own table with a One-To-One relationship with the existing User Model
"""

UserModel = get_user_model()


class Profile(models.Model):
    COUNTRIES_MAX_LENGTH = 50
    COUNTRIES_MIN_LENGTH = 4

    MAX_IMAGE_SIZE_IN_MB = 1

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    profile_picture = cloudinary_models.CloudinaryField(
        null=True,
        blank=True,
        verbose_name='Profile Picture',
        use_filename=True,
        validators=(
            ImageSizeInMBValidator(MAX_IMAGE_SIZE_IN_MB),
        )
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name='Date of Birth',
    )

    current_country = models.CharField(
        null=True,
        blank=True,
        max_length=COUNTRIES_MAX_LENGTH,
        validators=(
            MinLengthValidator(COUNTRIES_MIN_LENGTH),
        ),
        verbose_name='Current Country',
    )

    def __str__(self):
        return f"{self.user}'s Profile"

    def save(self, *args, **kwargs):
        if self.current_country:
            self.current_country = self.current_country.title()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


@receiver(signals.post_save, sender=UserModel)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(signals.post_delete, sender=Profile)
def delete_profile_user(sender, instance, **kwargs):
    def __remove_cloudinary_image(image):
        cloudinary.uploader.destroy(image.public_id, invalidate=True, )

    instance.user.delete()

    if instance.profile_picture:
        __remove_cloudinary_image(instance.profile_picture)
