from django.urls import path
from animal_rent_api.apps.animals.views import AnimalsListView, CreateAnimalView, GetAnimalInformationView, \
	RemoveAnimalView, MyAnimalsListView

urlpatterns = [
	path('', AnimalsListView.as_view(), name='animals_list'),
	path('my_animals/', MyAnimalsListView.as_view(), name='my_animal_list'),
	path('<int:id>', GetAnimalInformationView.as_view(), name='animals_retrieve'),
	path('remove/<int:id>', RemoveAnimalView.as_view(), name='remove_animal'),
	path('create/', CreateAnimalView.as_view(), name='create_animal')
]
