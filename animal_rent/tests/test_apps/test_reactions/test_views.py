from random import randint

import pytest
from rest_framework import status as rest_status

from animal_rent_api.apps.animals.facroties import AnimalFactory
from animal_rent_api.apps.reactions.models import Complaint
from animal_rent_api.apps.requests.constants import Statuses
from animal_rent_api.apps.requests.factories import RentRequestFactory
from tests.utils import post_data


def create_animal_with_blocked(user):
	return AnimalFactory(owner=user)


def create_rent_request(user, animal, status=Statuses.APPROVED):
	return RentRequestFactory(animal=animal, renter=user, status=status)


@pytest.mark.django_db
def test_create_complaint(user, second_user):
	complain_data = {
		"defendant": second_user.id,
		"text": "blablabla"
	}
	result = post_data(user=user, url='add_complaint', data=complain_data)
	assert result.status_code == rest_status.HTTP_201_CREATED
	complain = Complaint.objects.first()
	assert complain.complaint_creater == user


def _get_dict_for_review(animal, rating):
	return {
		"animal": animal.id,
		"text": "jpieqwuf",
		"rating": rating
	}


@pytest.mark.django_db
def test_create_review_ok(user, second_user):
	animal = create_animal_with_blocked(user=second_user)
	create_rent_request(user, animal)
	rating = randint(1, 5)
	dict_for_creation = _get_dict_for_review(animal, rating)
	result = post_data(user=user, url='add_comment', data=dict_for_creation)
	assert result.status_code == rest_status.HTTP_201_CREATED
	animal.refresh_from_db()
	assert animal.rating == rating


@pytest.mark.django_db
def test_create_review_fail(user, second_user):
	animal = create_animal_with_blocked(user=second_user)
	create_rent_request(user, animal)
	rating = randint(1, 5)
	dict_for_creation = _get_dict_for_review(animal, rating)
	dict_for_creation.pop('rating')
	dict_for_creation.pop('text')
	result = post_data(user=user, url='add_comment', data=dict_for_creation)
	assert result.status_code == rest_status.HTTP_400_BAD_REQUEST
	new_animal = create_animal_with_blocked(user=second_user)
	dict_for_creation = _get_dict_for_review(new_animal, rating)
	result = post_data(user=user, url='add_comment', data=dict_for_creation)
	assert result.status_code == rest_status.HTTP_400_BAD_REQUEST
	rating = randint(10, 20)
	dict_for_creation = _get_dict_for_review(animal, rating)
	result = post_data(user=user, url='add_comment', data=dict_for_creation)
	assert result.status_code == rest_status.HTTP_400_BAD_REQUEST
