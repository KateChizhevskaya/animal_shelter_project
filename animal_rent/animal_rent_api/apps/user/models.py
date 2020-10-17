from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField, OneToOneField, CASCADE
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from animal_rent_api.apps.user.constants import UserRoleEnum


class RentUser(AbstractUser):
	is_deleted = BooleanField(default=False)
	phone_number = PhoneNumberField(
		help_text='Contact phone number',
		null=True,
		region='BY'
	)
	role = models.CharField(
		max_length=20,
		choices=UserRoleEnum.choices,
		default=UserRoleEnum.INDIVIDUAL
	)
