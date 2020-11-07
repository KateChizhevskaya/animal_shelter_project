import factory
from django.utils import timezone
from animal_rent_api.apps.requests.constants import Statuses, PERIOD_FOR_TESTS
from animal_rent_api.apps.requests.models import AddAnimalForRentRequest, RentRequest


class AddAnimalForRentRequestFactory(factory.django.DjangoModelFactory):
	status = Statuses.APPROVED
	text_comment = factory.Faker('pystr', max_chars=10)

	class Meta:
		model = AddAnimalForRentRequest


class RentRequestFactory(factory.django.DjangoModelFactory):
	date_time_of_rent_begin = timezone.now()
	date_time_of_rent_end = timezone.now() + PERIOD_FOR_TESTS
	status = Statuses.APPROVED
	renter_text_comment = factory.Faker('pystr', max_chars=10)

	class Meta:
		model = RentRequest
