from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework import serializers
from animal_rent_api.apps.animals.filters import AnimalFilter
from animal_rent_api.apps.animals.models import Animal
from animal_rent_api.apps.animals.serializers import AnimalListSerializer, AnimalCreateSerializer, \
	RetrieveAnimalSerializer


class AnimalsListView(generics.ListAPIView):
	serializer_class = AnimalListSerializer
	filter_backends = (DjangoFilterBackend, )
	filterset_class = AnimalFilter
	queryset = Animal.objects.filter(blocked=False, owner__is_deleted=False)


class CreateAnimalView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, )
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
