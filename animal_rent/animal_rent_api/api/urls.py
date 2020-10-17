from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from animal_rent_api.api.app_urls import urls

app_name = 'api'

urlpatterns = [
	path('rent/', include(urls.urlpatterns))
]
