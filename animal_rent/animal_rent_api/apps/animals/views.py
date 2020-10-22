from django.http import Http404
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
	serializer_class = RetrieveAnimalSerializer

	def get_object(self):
		try:
			return Animal.objects.raw(
				f'''SELECT "apps_animal"."id", "apps_animal"."animal_type", "apps_animal"."breed",
				"apps_animal"."height", "apps_animal"."weight", "apps_animal"."delivery_type",
				"apps_animal"."rating", "apps_animal"."description", "apps_animal"."owner_id",
				"apps_animal"."portfolio_id", "apps_animal"."price",
				"apps_animal"."price_for_business",
				"apps_animal"."animal_name" FROM "apps_animal" INNER JOIN "apps_rentuser" ON
				("apps_animal"."owner_id" = "apps_rentuser"."id") INNER JOIN "apps_portfolio" ON
				("apps_animal"."portfolio_id" = "apps_portfolio"."id") WHERE
				("apps_animal"."blocked" = False AND "apps_rentuser"."is_deleted" = False AND apps_animal.id = {self.request.parser_context["kwargs"]["id"]})'''
			)[0]
		except IndexError:
			raise Http404


class RemoveAnimalView(generics.DestroyAPIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get_object(self):
		try:
			return Animal.objects.raw(
				f'''SELECT * FROM "apps_animal" WHERE
			("apps_animal"."owner_id" = {self.request.user.id} AND apps_animal.id = {self.request.parser_context["kwargs"]["id"]})'''
			)[0]
		except IndexError:
			raise serializers.ValidationError(
				'You can not delete that animal'
			)

	def perform_destroy(self, instance):
		instance.blocked = True
		instance.save(update_fields=['blocked'])
