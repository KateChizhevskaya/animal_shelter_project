from django.urls import path
from animal_rent_api.apps.user.views import RegistrationView, LoginView

urlpatterns = [
	path('registrate/', RegistrationView.as_view(), name='registration'),
	path('login/', LoginView.as_view(), name='login')
]
