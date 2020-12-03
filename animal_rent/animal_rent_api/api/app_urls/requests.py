from django.urls import path

from animal_rent_api.apps.requests.views import AddAnimalForRentAnswerView, RentRequestCreateView, \
	RentRequestAnswerView, RentRequestListView, RentRequestRetrieveView, AddAnimalForRentListView, \
	AddAnimalForRentRetrieveView, MyRentRequestListView, MyAddAnimalForRentListView

urlpatterns = [
	path('answer/add_animal_for_rent/<int:id>/', AddAnimalForRentAnswerView.as_view(), name='answer_add_animal_for_rent'),
	path('get_animal_for_rent/', RentRequestCreateView.as_view(), name='animal_rent_request'),
	path('my_add_animal_for_rent/', MyAddAnimalForRentListView.as_view(), name='my_list_add_animal_for_rent_request'),
	path('my_rent_request/', MyRentRequestListView.as_view(), name='my_list_rent_request'),
	path('answer/rent_request/<int:id>/', RentRequestAnswerView.as_view(), name='answer_rent_request'),
	path('rent_request/<int:id>/', RentRequestRetrieveView.as_view(), name='retrieve_rent_request'),
	path('rent_request/', RentRequestListView.as_view(), name='list_rent_request'),
	path('add_animal_for_rent/<int:id>/', AddAnimalForRentRetrieveView.as_view(), name='retrieve_add_animal_for_rent_request'),
	path('add_animal_for_rent/', AddAnimalForRentListView.as_view(), name='list_add_animal_for_rent_request'),
]
