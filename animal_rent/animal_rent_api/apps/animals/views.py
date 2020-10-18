from rest_framework import generics, permissions
from rest_framework import serializers
from animal_rent_api.apps.animals.models import Animal
from animal_rent_api.apps.animals.serializers import AnimalListSerializer, AnimalCreateSerializer, \
	RetrieveAnimalSerializer


class AnimalsListView(generics.ListAPIView):
	serializer_class = AnimalListSerializer
	queryset = Animal.objects.raw(
		'SELECT "apps_animal"."id", "apps_animal"."animal_type", "apps_animal"."breed",'
		' "apps_animal"."height", "apps_animal"."weight", "apps_animal"."delivery_type", '
		'"apps_animal"."rating", "apps_animal"."description", "apps_animal"."owner_id", '
		'"apps_animal"."portfolio_id", "apps_animal"."price", '
		'"apps_animal"."price_for_business",'
		' "apps_animal"."animal_name" FROM "apps_animal" INNER JOIN "apps_rentuser" ON '
		'("apps_animal"."owner_id" = "apps_rentuser"."id") WHERE '
		'("apps_animal"."blocked" = False AND "apps_rentuser"."is_deleted" = False)'
	)


class CreateAnimalView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = AnimalCreateSerializer


class GetAnimalInformationView(generics.RetrieveAPIView):
	lookup_field = 'id'
	serializer_class = RetrieveAnimalSerializer
	queryset = Animal.objects.filter(blocked=False, owner__is_deleted=False)


class RemoveAnimalView(generics.DestroyAPIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get_object(self):
		try:
			return Animal.objects.get(id=self.kwargs['id'], owner=self.request.user)
		except Animal.DoesNotExist:
			raise serializers.ValidationError(
				'You can not delete that animal'
			)

	def perform_destroy(self, instance):
		instance.blocked = True
		instance.save(update_fields=['blocked'])
