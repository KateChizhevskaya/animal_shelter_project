from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CASCADE, SET_NULL
from django.db import models

from animal_rent_api.apps.animals.models import Animal
from animal_rent_api.apps.requests.constants import Statuses
from animal_rent_api.apps.user.models import RentUser


class Review(models.Model):
	animal = models.ForeignKey(
		Animal,
		related_name='reviews',
		on_delete=CASCADE
	)
	user = models.ForeignKey(
		RentUser,
		related_name='reviews',
		on_delete=CASCADE
	)
	text = models.TextField(
		max_length=500,
		null=True,
		blank=True
	)
	rating = models.IntegerField(
		validators=[MinValueValidator(0), MaxValueValidator(5)],
		null=True
	)


class Complaint(models.Model):
	complaint_creater = models.ForeignKey(
		RentUser,
		related_name='complaints_created',
		on_delete=CASCADE
	)
	defendant = models.ForeignKey(
		RentUser,
		related_name='complaints_defendant',
		on_delete=SET_NULL,
		null=True
	)
	text = models.TextField(
		max_length=500
	)

