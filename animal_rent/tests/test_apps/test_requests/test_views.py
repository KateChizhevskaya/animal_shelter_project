import pytest
from django.utils import timezone
from rest_framework import status as rest_status

from animal_rent_api.apps.animals.facroties import AnimalFactory
from animal_rent_api.apps.requests.constants import PERIOD_FOR_TESTS, INCORRECT_PERIOD_FOR_TESTS
from animal_rent_api.apps.requests.models import RentRequest
from tests.utils import post_data


def create_animal_with_blocked(user, blocked=False):
	return AnimalFactory(blocked=blocked, owner=user)


def get_base_rent_request(user):
	animal = create_animal_with_blocked(user=user)
	return {
		"animal": animal.id,
		"date_time_of_rent_begin": timezone.now(),
		"renter_text_comment": "ajncd"
	}


def correct_time_rent_request(user):
	base_rent_request = get_base_rent_request(user)
	base_rent_request["date_time_of_rent_end"] = base_rent_request["date_time_of_rent_begin"] + PERIOD_FOR_TESTS
	return base_rent_request


def incorrect_time_rent_request(user):
	base_rent_request = get_base_rent_request(user)
	base_rent_request["date_time_of_rent_end"] = base_rent_request["date_time_of_rent_begin"] + INCORRECT_PERIOD_FOR_TESTS
	return base_rent_request


@pytest.mark.django_db
def test_create_rent_request_ok(user):
	request = correct_time_rent_request(user)
	response = post_data(user, 'animal_rent_request', data=request)
	assert response .status_code == rest_status.HTTP_201_CREATED
	assert RentRequest.objects.count() == 1


@pytest.mark.django_db
def test_create_rent_request_failed(user):
	request = incorrect_time_rent_request(user)
	response = post_data(user, 'animal_rent_request', data=request)
	assert response .status_code == rest_status.HTTP_400_BAD_REQUEST
