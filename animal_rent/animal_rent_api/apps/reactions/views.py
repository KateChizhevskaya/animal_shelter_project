from rest_framework import generics, permissions

from animal_rent_api.apps.reactions.serializers import AddReviewSerializer, AddComplaintSerializer


class AddReviewView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = AddReviewSerializer


class AddComplaint(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = AddComplaintSerializer

