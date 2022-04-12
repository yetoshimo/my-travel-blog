# Generated by Django 4.0.3 on 2022-04-12 15:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitedCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=64, verbose_name='City Name')),
                ('country_name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(4)], verbose_name='Country Name')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
                'ordering': ('city_name', 'country_name'),
                'unique_together': {('user', 'city_name', 'country_name')},
            },
        ),
        migrations.CreateModel(
            name='VisitedHotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=64, verbose_name='Hotel Name')),
                ('number_of_stars', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1, verbose_name='Number of Stars')),
                ('star_count', models.CharField(max_length=20, verbose_name='Star Count')),
                ('located_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.visitedcity', verbose_name='Located City')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Hotel',
                'verbose_name_plural': 'Hotels',
                'ordering': ('hotel_name', 'located_city'),
                'unique_together': {('user', 'located_city', 'hotel_name')},
            },
        ),
        migrations.CreateModel(
            name='TravelPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True)),
                ('travel_picture', models.URLField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(200)])),
                ('uploaded_on', models.DateTimeField(auto_now_add=True)),
                ('located_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.visitedcity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Travel Picture',
                'verbose_name_plural': 'Travel Pictures',
            },
        ),
        migrations.CreateModel(
            name='TravelEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Entry Title')),
                ('description', models.TextField(blank=True, null=True)),
                ('publish_date_time', models.DateTimeField(auto_now_add=True)),
                ('travel_picture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.travelpicture')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('visited_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.visitedcity')),
                ('visited_hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.visitedhotel')),
            ],
            options={
                'verbose_name': 'Travel Entry',
                'verbose_name_plural': 'Travel Entries',
            },
        ),
    ]
