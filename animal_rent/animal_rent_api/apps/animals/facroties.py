import factory

from animal_rent_api.apps.animals.constants import AnimalType, DeliveryType
from animal_rent_api.apps.animals.models import Animal
from animal_rent_api.apps.user.factories import UserFactory


class AnimalFactory(factory.django.DjangoModelFactory):
	animal_type = AnimalType.CAT
	breed = factory.Faker('pystr', max_chars=10)
	height = factory.Faker(
		'random_int', min=11, max=170
	)
	weight = factory.Faker(
		'random_int', min=1, max=100
	)
	delivery_type = DeliveryType.PICKUP
	rating = factory.Faker(
		'random_int', min=1, max=4
	)
	description = factory.Faker('pystr', max_chars=20)
	portfolio = None
	price = factory.Faker(
		'random_int', min=11, max=170
	)
	price_for_business = factory.Faker(
		'random_int', min=11, max=170
	)
	blocked = False
	animal_name = factory.Faker('pystr', max_chars=10)

	class Meta:
		model = Animal
