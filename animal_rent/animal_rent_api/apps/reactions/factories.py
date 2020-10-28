import factory
from animal_rent_api.apps.reactions.models import Review, Complaint


class ReviewFactory(factory.django.DjangoModelFactory):
	text = factory.Faker('pystr', max_chars=10)
	rating = factory.Faker(
		'random_int', min=1, max=5
	)

	class Meta:
		model = Review


class ComplaintFactory(factory.django.DjangoModelFactory):
	text = factory.Faker('pystr', max_chars=10)

	class Meta:
		model = Complaint
