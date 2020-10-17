from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from animal_rent_api.apps.requests.constants import Statuses
from animal_rent_api.apps.requests.models import AddAnimalForRentRequest, RentRequest
from animal_rent_api.apps.requests.serializers import AnswerAddAnimalForRentRequestSerializer, \
	CreateRentAnimalRequestSerializer, AnswerForRentRequestSerializer, RentRequestViewSerializer, \
	AddAnimalForRentRequestViewSerializer


class AddAnimalForRentAnswerView(generics.UpdateAPIView):
	lookup_field = 'id'
	serializer_class = AnswerAddAnimalForRentRequestSerializer
	queryset = AddAnimalForRentRequest.objects.filter(status=Statuses.IN_PROCESS)
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)


class AddAnimalForRentListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
	serializer_class = AddAnimalForRentRequestViewSerializer
	filter_backends = [DjangoFilterBackend, ]
	filterset_fields = ['status', ]
	queryset = AddAnimalForRentRequest.objects.all()


class AddAnimalForRentRetrieveView(generics.RetrieveAPIView):
	serializer_class = AddAnimalForRentRequestViewSerializer
	filter_backends = [DjangoFilterBackend, ]
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
	lookup_field = 'id'
	queryset = AddAnimalForRentRequest.objects.all()


class RentRequestAnswerView(generics.UpdateAPIView):
	lookup_field = 'id'
	serializer_class = AnswerForRentRequestSerializer
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

	def get_queryset(self):
		return RentRequest.objects.filter(status=Statuses.IN_PROCESS, animal__owner=self.request.user)


class RentRequestCreateView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = CreateRentAnimalRequestSerializer


class RentRequestListView(generics.ListAPIView):
	serializer_class = RentRequestViewSerializer
	filter_backends = [DjangoFilterBackend, ]
	filterset_fields = ['status', ]
	permission_classes = (permissions.IsAuthenticated, )

	def get_queryset(self):
		return RentRequest.objects.filter(animal__owner=self.request.user)


class RentRequestRetrieveView(generics.RetrieveAPIView):
	serializer_class = RentRequestViewSerializer
	filter_backends = [DjangoFilterBackend, ]
	filterset_fields = ['status', ]
	permission_classes = (permissions.IsAuthenticated, )
	lookup_field = 'id'

	def get_queryset(self):
		return RentRequest.objects.filter(animal__owner=self.request.user)
