import random
from rest_framework import status as rest_status
import pytest

from animal_rent_api.apps.additional_documents.models import Portfolio
from animal_rent_api.apps.animals.constants import DANGEROUS_BREEDS
from animal_rent_api.apps.animals.facroties import AnimalFactory
from animal_rent_api.apps.animals.models import Animal
from tests.utils import get_response, del_response, post_data


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


def prepare_dict_for_animal_add():
	return {
		"animal_name": "kate1",
		"description": "aaaab",
		"portfolio": {
			"awards": "aa, abb",
			"past_photo_places": "bb, cc",
			"additional_description": "abc"
		},
		"animal_type": "cat",
		"breed": "bca",
		"height": 20,
		"weight": 20,
		"delivery_type": "delivery",
		"price": 10,
		"price_for_business": 20
	}


@pytest.mark.django_db
def test_ok_add_animal(user):
	animal_add_info = prepare_dict_for_animal_add()
	result = post_data(user=user, url='create_animal', data=animal_add_info, format='json')
	assert result.status_code == rest_status.HTTP_201_CREATED
	animal = Animal.objects.first()
	assert animal.blocked
	assert animal.owner == user
	assert animal.price == animal_add_info['price']
	portfolio = Portfolio.objects.first()
	assert animal.portfolio == portfolio


@pytest.mark.django_db
def test_fail_add_animal(user):
	animal_add_info = prepare_dict_for_animal_add()
	animal_add_info['breed'] = list(DANGEROUS_BREEDS)[0]
	result = post_data(user=user, url='create_animal', data=animal_add_info, format='json')
	assert result.status_code == rest_status.HTTP_400_BAD_REQUEST
