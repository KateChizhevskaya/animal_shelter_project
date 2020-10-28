import random
from rest_framework import status as rest_status
import pytest

from animal_rent_api.apps.animals.facroties import AnimalFactory
from tests.utils import get_response, del_response


def create_n_animal(n, user):
	for i in range(n):
		AnimalFactory(owner=user)


def create_animal_with_blocked(user, blocked=False):
	return AnimalFactory(blocked=blocked, owner=user)


@pytest.mark.django_db
def test_animal_list(user):
	n = random.randint(1, 5)
	create_n_animal(n, user)
	result = get_response(user, 'animals_list', data={})
	assert result.status_code == rest_status.HTTP_200_OK
	assert result.data['count'] == n


@pytest.mark.django_db
def test_retrieve_animal_ok(user):
	animal = create_animal_with_blocked(user)
	result = get_response(user, 'animals_retrieve', data={}, id=animal.id)
	assert result.status_code == rest_status.HTTP_200_OK
	assert result.data['id'] == animal.id


@pytest.mark.django_db
def test_retrieve_animal_failed(user, blocked_user):
	blocked_animal = create_animal_with_blocked(user, True)
	result = get_response(user, 'animals_retrieve', data={}, id=blocked_animal.id)
	assert result.status_code == rest_status.HTTP_404_NOT_FOUND
	blocked_user_for_animal = create_animal_with_blocked(blocked_user)
	result = get_response(user, 'animals_retrieve', data={}, id=blocked_user_for_animal.id)
	assert result.status_code == rest_status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_remove_animal_ok(user):
	animal = create_animal_with_blocked(user)
	result = del_response(user, 'remove_animal', data={}, id=animal.id)
	animal.refresh_from_db()
	assert result.status_code == rest_status.HTTP_204_NO_CONTENT
	assert animal.blocked


@pytest.mark.django_db
def test_remove_animal_fail(user, second_user):
	animal = create_animal_with_blocked(user)
	result = del_response(second_user, 'remove_animal', data={}, id=animal.id)
	animal.refresh_from_db()
	assert result.status_code == rest_status.HTTP_400_BAD_REQUEST
	assert not animal.blocked
