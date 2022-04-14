# Generated by Django 4.0.3 on 2022-04-14 14:22

import cloudinary.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mytravelblog.common.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_picture', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, validators=[mytravelblog.common.validators.ImageSizeInMBValidator(3)], verbose_name='Profile Picture')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('current_country', models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.MinLengthValidator(4)], verbose_name='Current Country')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
