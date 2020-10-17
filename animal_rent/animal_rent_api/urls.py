from animal_rent_api.api import urls as api_urls
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', include(api_urls.urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

