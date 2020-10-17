from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CASCADE, SET_NULL
from django.db import models

from animal_rent_api.apps.additional_documents.models import Portfolio
from animal_rent_api.apps.animals.constants import AnimalType, DeliveryType

from animal_rent_api.apps.user.models import RentUser


class Animal(models.Model):
	animal_type = models.CharField(
		max_length=10,
		choices=AnimalType.choices,
	)
	breed = models.CharField(
		max_length=50
	)
	height = models.IntegerField(
		validators=[MinValueValidator(10), MaxValueValidator(180)]
	)
	weight = models.FloatField(
		validators=[MinValueValidator(0.005), MaxValueValidator(120)]
	)
	delivery_type = models.CharField(
		max_length=10,
		choices=DeliveryType.choices,
		default=DeliveryType.PICKUP
	)
	rating = models.FloatField(
		validators=[MinValueValidator(0), MaxValueValidator(5)],
		default=0
	)
	description = models.TextField(
		max_length=500,
		blank=True,
		null=True
	)
	owner = models.ForeignKey(
		RentUser,
		related_name='animals',
		on_delete=CASCADE,
	)
	portfolio = models.OneToOneField(
		Portfolio,
		related_name='animal',
		on_delete=SET_NULL,
		null=True
	)
	price = models.FloatField(
		validators=[MinValueValidator(0.005), MaxValueValidator(5000)]
	)
	price_for_business = models.FloatField(
		validators=[MinValueValidator(0.005), MaxValueValidator(5000)]
	)
	blocked = models.BooleanField(
		default=True
	)
	animal_name = models.CharField(
		max_length=100,
		blank=True,
		null=True
	)

	class Meta:
		unique_together = ('animal_type', 'breed', 'owner', 'animal_name')

