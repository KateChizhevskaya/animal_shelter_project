from typing import AnyStr, Dict

from django.urls import resolve
from rest_framework import reverse as rest_reverse
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient

from animal_rent_api.apps.user.models import RentUser


def get_response(user: RentUser, url: AnyStr, data: Dict = None) -> Response:
	rest_request_factory = APIRequestFactory()
	request = rest_request_factory.get(url, data=data, format='json')
	force_authenticate(request, user)
	view, _, _ = resolve(url)
	response = view(request)
	return response


def post_data(user, url, data=None):
	rest_request_factory = APIRequestFactory()
	request = rest_request_factory.post(url, data=data, format='json')
	force_authenticate(request, user)
	view, _, _ = resolve(url)
	response = view(request)
	return response


def put_data(user, url, data=None, request_format='json'):
	rest_request_factory = APIClient()
	rest_request_factory.force_authenticate(user)
	response = rest_request_factory.put(url, data=data, format=request_format)
	return response


def patch_data(user, url, data=None):
	rest_request_factory = APIClient()
	rest_request_factory.force_authenticate(user)
	response = rest_request_factory.patch(url, data=data, format='json')
	return response
