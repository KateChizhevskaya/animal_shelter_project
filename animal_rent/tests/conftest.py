import pytest

from animal_rent_api.apps.user.factories import UserFactory


@pytest.fixture
def user():
	return UserFactory()


@pytest.fixture
def second_user():
	return UserFactory()


@pytest.fixture
def blocked_user():
	return UserFactory(is_deleted=True)


@pytest.fixture
def admin_user():
	return UserFactory(is_staff=True)
