from animal_rent_api.apps.user.models import RentUser
import factory


class UserFactory(factory.django.DjangoModelFactory):
	email = factory.Faker('email')
	username = factory.Faker('email')
	password = factory.PostGenerationMethodCall('set_password', 'kate_user')
	first_name = factory.Faker('first_name')
	last_name = factory.Faker('last_name')
	is_staff = False
	is_active = True
	is_superuser = False

	class Meta:
		model = RentUser
