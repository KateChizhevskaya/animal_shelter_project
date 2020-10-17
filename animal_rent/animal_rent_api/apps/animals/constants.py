from django.db import models
from django.utils.translation import gettext_lazy as _


class AnimalType(models.TextChoices):

	CAT = 'cat', _('Cat')
	DOG = 'dog', _('dog')
	PARROT = 'parrot', _('Parrot')


class DeliveryType(models.TextChoices):

	PICKUP = 'pickup', _('Pickup')
	DELIVERY = 'delivery', _('Delivery')


DANGEROUS_BREEDS = {'Sheepherd', }
ADD_ANIMAL_HEADER = 'Animal add request'
ADD_ANIMAL_TEXT = 'Somebody want to add animal for renting, check it please'
ANIMAL_PHOTOS_FOLDER = "animals_photos"
MEDICAL_FILES_FOLDER = "medical_files"
