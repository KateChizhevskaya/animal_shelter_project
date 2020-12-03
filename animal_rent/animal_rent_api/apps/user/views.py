from django.http import Http404
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
		try:
			return RentUser.objects.raw(
				f'''
					SELECT "apps_rentuser"."id", "apps_rentuser"."password","apps_rentuser"."phone_number"
					FROM "apps_rentuser" WHERE ("apps_rentuser"."id" = {self.request.user.id} AND "apps_rentuser"."is_deleted" = False)
				'''
			)[0]
		except IndexError:
			raise Http404


class UserListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
	queryset = RentUser.objects.raw(
		f'''
			SELECT * FROM "apps_rentuser"
		'''
	)
	serializer_class = UserListChangeStatusSerializer


class ChangeUserBlockedStatusView(generics.UpdateAPIView):
	serializer_class = UserListChangeStatusSerializer
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

	def get_object(self):
		try:
			return RentUser.objects.raw(
				f'''
							SELECT "apps_rentuser"."id", "apps_rentuser"."is_deleted"
							FROM "apps_rentuser" WHERE ("apps_rentuser"."id" = {self.request.parser_context["kwargs"]["id"]})
						'''
			)[0]
		except IndexError:
			raise Http404
