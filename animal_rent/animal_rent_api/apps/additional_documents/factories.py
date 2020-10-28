import factory

from animal_rent_api.apps.additional_documents.models import Portfolio


class PortfolioFactory(factory.django.DjangoModelFactory):
	additional_description = factory.Faker('pystr', max_chars=10)
	awards = factory.Faker('pystr', max_chars=20)
	past_photo_places = factory.Faker('pystr', max_chars=10)

	class Meta:
		model = Portfolio
