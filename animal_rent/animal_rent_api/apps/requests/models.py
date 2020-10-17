from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CASCADE, SET_NULL
from django.db import models
from phone_field import PhoneField

from animal_rent_api.apps.animals.models import Animal
from animal_rent_api.apps.requests.constants import Statuses
from animal_rent_api.apps.user.models import RentUser


class AddAnimalForRentRequest(models.Model):
	lessor = models.ForeignKey(
		RentUser,
		related_name='add_animal_application',
		on_delete=SET_NULL,
		null=True
	)
	status = models.CharField(
		max_length=20,
		choices=Statuses.choices,
		default=Statuses.IN_PROCESS
	)
	animal = models.ForeignKey(
		Animal,
		related_name='add_animal_application',
		on_delete=SET_NULL,
		null=True
	)
	text_comment = models.TextField(
		max_length=100,
		blank=True,
		null=True,
		default=None
	)
	date_of_creating_request = models.DateTimeField(
		auto_now_add=True
	)


class RentRequest(models.Model):
	animal = models.ForeignKey(
		Animal,
		related_name='rent_requests',
		on_delete=SET_NULL,
		null=True
	)
	renter = models.ForeignKey(
		RentUser,
		related_name='rent_requests',
		on_delete=CASCADE
	)
	date_of_creating_request = models.DateTimeField(
		auto_now_add=True
	)
	date_time_of_rent_begin = models.DateTimeField()
	date_time_of_rent_end = models.DateTimeField()
	status = models.CharField(
		max_length=20,
		choices=Statuses.choices,
		default=Statuses.IN_PROCESS
	)
	renter_text_comment = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		default=None
	)
	phone_number = PhoneField(
		help_text='Contact phone number',
		null=True,
		blank=True
	)
