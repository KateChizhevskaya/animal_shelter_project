import pytest
import random
import string
from rest_framework import status as rest_status

from animal_rent_api.apps.animals.facroties import AnimalFactory
from animal_rent_api.apps.requests.constants import PERIOD_FOR_TESTS, INCORRECT_PERIOD_FOR_TESTS, Statuses
from animal_rent_api.apps.requests.factories import AddAnimalForRentRequestFactory
from animal_rent_api.apps.requests.models import RentRequest
from tests.utils import post_data, patch_data


def update_dict_for_user(new_password, new_phone_number, old_password):
	return {
		"phone_number": new_phone_number,
		"new_password": new_password,
		"repeated_new_password": new_password,
		"password": old_password
	}


def get_delete_dict_for_user():
	return {
		"is_deleted": True
	}


def get_random_string(length):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))


def get_dict_for_update(user):
	length = random.randint(1, 10)
	new_phone_number = "+375297603585"
	new_password = get_random_string(length)
	old_password = get_random_string(length)
	user.set_password(old_password)
	user.save()
	return update_dict_for_user(new_password, new_phone_number, old_password)


@pytest.mark.django_db
def test_update_user_ok(user):
	correct_dict = get_dict_for_update(user)
	response = patch_data(user, 'update_user', data=correct_dict)
	assert response.status_code == rest_status.HTTP_200_OK
	user.refresh_from_db()
	assert user.phone_number == correct_dict['phone_number']


@pytest.mark.django_db
def test_update_only_phone_user_ok(user):
	correct_dict = get_dict_for_update(user)
	correct_dict_with_only_phone = {
		"phone_number": correct_dict['phone_number']
	}
	response = patch_data(user, 'update_user', data=correct_dict_with_only_phone)
	assert response.status_code == rest_status.HTTP_200_OK
	user.refresh_from_db()
	assert user.phone_number == correct_dict['phone_number']


@pytest.mark.django_db
def test_update_user_fail(user):
	correct_dict = get_dict_for_update(user)
	length = random.randint(1, 10)
	correct_dict['repeated_new_password'] = get_random_string(length)
	response = patch_data(user, 'update_user', data=correct_dict)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST
	correct_dict = get_dict_for_update(user)
	correct_dict.pop('password')
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_user_ok(admin_user, user):
	correct_dict = get_delete_dict_for_user()
	response = patch_data(admin_user, 'change_blocked_status', data=correct_dict, id=user.id)
	assert response.status_code == rest_status.HTTP_200_OK
	user.refresh_from_db()
	assert user.is_deleted


@pytest.mark.django_db
def test_delete_user_failed(admin_user, user):
	correct_dict = get_delete_dict_for_user()
	response = patch_data(user, 'change_blocked_status', data=correct_dict, id=user.id)
	assert response.status_code == rest_status.HTTP_403_FORBIDDEN
	response = patch_data(admin_user, 'change_blocked_status', data=correct_dict, id=user.id+random.randint(1, 10))
	assert response.status_code == rest_status.HTTP_404_NOT_FOUND
