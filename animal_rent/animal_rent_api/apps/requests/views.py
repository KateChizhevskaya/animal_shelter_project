from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from animal_rent_api.apps.requests.models import AddAnimalForRentRequest, RentRequest
from animal_rent_api.apps.requests.serializers import AnswerAddAnimalForRentRequestSerializer, \
	CreateRentAnimalRequestSerializer, AnswerForRentRequestSerializer, RentRequestViewSerializer, \
	AddAnimalForRentRequestViewSerializer


class AddAnimalForRentAnswerView(generics.UpdateAPIView):
	serializer_class = AnswerAddAnimalForRentRequestSerializer
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

	def get_object(self):
		try:
			return AddAnimalForRentRequest.objects.raw(
					f'''SELECT apps_addanimalforrentrequest.id FROM apps_addanimalforrentrequest WHERE
				(apps_addanimalforrentrequest.id = {self.request.parser_context["kwargs"]["id"]})'''
				)[0]
		except IndexError:
			raise Http404


class AddAnimalForRentListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
	serializer_class = AddAnimalForRentRequestViewSerializer
	queryset = AddAnimalForRentRequest.objects.raw(
				f'''SELECT * FROM apps_addanimalforrentrequest'''
			)


class MyAddAnimalForRentListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = AddAnimalForRentRequestViewSerializer

	def get_queryset(self):
		return AddAnimalForRentRequest.objects.raw(
					f'''SELECT * FROM apps_addanimalforrentrequest WHERE
				(apps_addanimalforrentrequest.lessor_id= {self.request.user.id})'''
				)


class AddAnimalForRentRetrieveView(generics.RetrieveAPIView):
	serializer_class = AddAnimalForRentRequestViewSerializer
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

	def get_object(self):
		try:
			return AddAnimalForRentRequest.objects.raw(
					f'''SELECT apps_addanimalforrentrequest.id FROM apps_addanimalforrentrequest WHERE
				(apps_addanimalforrentrequest.id = {self.request.parser_context["kwargs"]["id"]})'''
				)[0]
		except IndexError:
			raise Http404


class RentRequestAnswerView(generics.UpdateAPIView):
	serializer_class = AnswerForRentRequestSerializer
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

	def get_object(self):
		try:
			return RentRequest.objects.raw(
				f'''SELECT "apps_rentrequest"."id", "apps_rentrequest"."animal_id", "apps_rentrequest"."renter_id", 
				"apps_rentrequest"."date_of_creating_request", "apps_rentrequest"."date_time_of_rent_begin",
				"apps_rentrequest"."date_time_of_rent_end", "apps_rentrequest"."status", "apps_rentrequest"."renter_text_comment",
				"apps_rentrequest"."phone_number" FROM "apps_rentrequest" INNER JOIN "apps_animal" 
				ON ("apps_rentrequest"."animal_id" = "apps_animal"."id") WHERE
				("apps_animal"."owner_id" = {self.request.user.id} AND "apps_rentrequest"."id" = {self.request.parser_context["kwargs"]["id"]})'''
			)[0]
		except IndexError:
			raise Http404


class RentRequestCreateView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = CreateRentAnimalRequestSerializer


class RentRequestListView(generics.ListAPIView):
	serializer_class = RentRequestViewSerializer
	permission_classes = (permissions.IsAuthenticated, )

	def get_queryset(self):
		return RentRequest.objects.raw(
			f'''SELECT "apps_rentrequest"."id", "apps_rentrequest"."animal_id", "apps_rentrequest"."renter_id", 
			"apps_rentrequest"."date_of_creating_request", "apps_rentrequest"."date_time_of_rent_begin",
			"apps_rentrequest"."date_time_of_rent_end", "apps_rentrequest"."status", "apps_rentrequest"."renter_text_comment",
			"apps_rentrequest"."phone_number" FROM "apps_rentrequest" INNER JOIN "apps_animal" 
			ON ("apps_rentrequest"."animal_id" = "apps_animal"."id") WHERE
			("apps_animal"."owner_id" = {self.request.user.id})'''
		)


class MyRentRequestListView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = RentRequestViewSerializer

	def get_queryset(self):
		return RentRequest.objects.raw(
			f'''SELECT "apps_rentrequest"."id", "apps_rentrequest"."animal_id", "apps_rentrequest"."renter_id", 
			"apps_rentrequest"."date_of_creating_request", "apps_rentrequest"."date_time_of_rent_begin",
			"apps_rentrequest"."date_time_of_rent_end", "apps_rentrequest"."status", "apps_rentrequest"."renter_text_comment",
			"apps_rentrequest"."phone_number" FROM "apps_rentrequest" INNER JOIN "apps_animal" 
			ON ("apps_rentrequest"."animal_id" = "apps_animal"."id") WHERE
			("apps_rentrequest"."renter_id" = {self.request.user.id})'''
		)


class RentRequestRetrieveView(generics.RetrieveAPIView):
	serializer_class = RentRequestViewSerializer
	permission_classes = (permissions.IsAuthenticated, )

	def get_object(self):
		try:
			return RentRequest.objects.raw(
				f'''SELECT * FROM "apps_rentrequest" INNER JOIN "apps_animal" 
						ON ("apps_rentrequest"."animal_id" = "apps_animal"."id") WHERE
						("apps_animal"."owner_id" = {self.request.user.id} AND "apps_rentrequest"."id" = {self.request.parser_context["kwargs"]["id"]})'''
			)[0]
		except IndexError:
			raise Http404
