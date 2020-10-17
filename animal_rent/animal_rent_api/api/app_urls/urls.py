from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from animal_rent_api.api.app_urls import authentification, animals, requests, reactions, users

app_name = 'app_urls'

urlpatterns = [
	path('authentification/', include(authentification.urlpatterns)),
	path('animals/', include(animals.urlpatterns)),
	path('requests/', include(requests.urlpatterns)),
	path('reactions/', include(reactions.urlpatterns)),
	path('users/', include(users.urlpatterns)),
]
