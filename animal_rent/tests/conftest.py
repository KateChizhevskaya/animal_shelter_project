import pytest

from animal_rent_api.apps.user.factories import UserFactory, AdminUserFactory


@pytest.fixture
def user():
	return UserFactory()


@pytest.fixture
def admin_user():
	return AdminUserFactory()

