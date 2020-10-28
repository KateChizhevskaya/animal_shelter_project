import pytest

from animal_rent_api.apps.animals.facroties import AnimalFactory
from animal_rent_api.apps.animals.models import Animal


def clean_all_animals():
	Animal.objects.all().delete()


def create_n_animal(n, user):
	animals = []
	for i in range(n):
		animals.append(AnimalFactory(owner=user))
	return animals


@pytest.mark.django_db
def test_animal_list():
	pass