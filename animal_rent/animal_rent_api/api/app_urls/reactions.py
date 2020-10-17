from django.urls import path

from animal_rent_api.apps.reactions.views import AddReviewView, AddComplaint

urlpatterns = [
	path('add_comment/', AddReviewView.as_view(), name='add_comment'),
	path('add_complaint/', AddComplaint.as_view(), name='add_complaint')
]
