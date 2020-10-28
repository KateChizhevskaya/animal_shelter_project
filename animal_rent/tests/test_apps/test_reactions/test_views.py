import pytest
from rest_framework import status as rest_status

from animal_rent_api.apps.animals.facroties import AnimalFactory


def create_animal_with_blocked(user):
	return AnimalFactory(owner=user)


@pytest.mark.django_db
def test_ok_create_complaint(user):
	pass

