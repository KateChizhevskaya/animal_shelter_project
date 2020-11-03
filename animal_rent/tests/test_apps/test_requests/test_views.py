import pytest
from django.utils import timezone
from rest_framework import status as rest_status

from animal_rent_api.apps.animals.facroties import AnimalFactory
from animal_rent_api.apps.requests.constants import PERIOD_FOR_TESTS, INCORRECT_PERIOD_FOR_TESTS, Statuses
from animal_rent_api.apps.requests.factories import AddAnimalForRentRequestFactory
from animal_rent_api.apps.requests.models import RentRequest
from tests.utils import post_data, patch_data


def add_animal_to_rent_request(user, animal, status):
	return AddAnimalForRentRequestFactory(status=status, animal=animal, lessor=user)


def create_animal_with_blocked(user, blocked=False):
	return AnimalFactory(blocked=blocked, owner=user)


def get_base_rent_request(user):
	animal = create_animal_with_blocked(user=user)
	return {
		"animal": animal.id,
		"date_time_of_rent_begin": timezone.now(),
		"renter_text_comment": "ajncd"
	}


def answer_to_add_animal_request(status):
	return {
		'status': status
	}


def correct_time_rent_request(user):
	base_rent_request = get_base_rent_request(user)
	base_rent_request["date_time_of_rent_end"] = base_rent_request["date_time_of_rent_begin"] + PERIOD_FOR_TESTS
	return base_rent_request


def incorrect_time_rent_request(user):
	base_rent_request = get_base_rent_request(user)
	base_rent_request["date_time_of_rent_end"] = base_rent_request["date_time_of_rent_begin"] + INCORRECT_PERIOD_FOR_TESTS
	return base_rent_request


def prepare_data_for_add_ro_rent_answer(user):
	animal = create_animal_with_blocked(user=user, blocked=True)
	request = add_animal_to_rent_request(status=Statuses.IN_PROCESS, animal=animal, user=user)
	return animal, request


@pytest.mark.django_db
def test_change_status_for_add_animal_request(admin_user):
	animal, request = prepare_data_for_add_ro_rent_answer(admin_user)
	answer_to_add_animal_for_rent_request = answer_to_add_animal_request(Statuses.APPROVED.value)
	response = patch_data(admin_user, 'answer_add_animal_for_rent', data=answer_to_add_animal_for_rent_request, id=request.id)
	assert response.status_code == rest_status.HTTP_200_OK
	animal.refresh_from_db()
	assert not animal.blocked


@pytest.mark.django_db
def test_not_admin_for_add_animal_request(user):
	animal, request = prepare_data_for_add_ro_rent_answer(user)
	answer_to_add_animal_for_rent_request = answer_to_add_animal_request(Statuses.APPROVED.value)
	response = patch_data(user, 'answer_add_animal_for_rent', data=answer_to_add_animal_for_rent_request, id=request.id)
	assert response.status_code == rest_status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_change_status_for_add_animal_request(admin_user):
	animal, request = prepare_data_for_add_ro_rent_answer(admin_user)
	answer_to_add_animal_for_rent_request = answer_to_add_animal_request(Statuses.REJECTED.value)
	response = patch_data(admin_user, 'answer_add_animal_for_rent', data=answer_to_add_animal_for_rent_request, id=request.id)
	assert response.status_code == rest_status.HTTP_200_OK
	animal.refresh_from_db()
	assert animal.blocked


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
