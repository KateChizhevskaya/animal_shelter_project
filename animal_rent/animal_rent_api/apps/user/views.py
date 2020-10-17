from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from animal_rent_api.apps.user.models import RentUser
from animal_rent_api.apps.user.serializers import RegistrationSerializer, LoginSerializer, UpdateUserSerializer, \
	UserListChangeStatusSerializer


class RegistrationView(generics.CreateAPIView):
	serializer_class = RegistrationSerializer


class LoginView(generics.CreateAPIView):
	serializer_class = LoginSerializer


class UpdateUser(generics.UpdateAPIView):
	serializer_class = UpdateUserSerializer
	permission_classes = (permissions.IsAuthenticated, )

	def get_object(self):
		return RentUser.objects.get(is_deleted=False, id=self.request.user.id)


class UserListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
	queryset = RentUser.objects.all()
	serializer_class = UserListChangeStatusSerializer


class ChangeUserBlockedStatusView(generics.UpdateAPIView):
	serializer_class = UserListChangeStatusSerializer
	lookup_field = 'id'
	filter_backends = [DjangoFilterBackend, ]
	filterset_fields = ['is_deleted', ]
	queryset = RentUser.objects.all()
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
