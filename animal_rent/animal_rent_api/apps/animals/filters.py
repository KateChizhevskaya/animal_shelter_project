import django_filters
from django.db.models import Q
from django_filters import rest_framework

from animal_rent_api.apps.animals.models import Animal
from animal_rent_api.apps.requests.constants import Statuses
from animal_rent_api.apps.requests.models import RentRequest


class AnimalFilter(django_filters.FilterSet):

	rent_date = rest_framework.IsoDateTimeFromToRangeFilter(
		required=False,
		method='animal_free_range'
	)

	class Meta:
		model = Animal
		fields = {
			'price': ['lt', 'gt'],
			'price_for_business': ['lt', 'gt'],
			'rating': ['lt', 'gt'],
			'delivery_type': ['in'],
			'animal_type': ['in'],
			'breed': ['in']
		}

	def animal_free_range(self, queryset, name, value):
		free_animals_ids = RentRequest.objects.filter(
			Q(animal__in=queryset) & Q(rent_requests__status=Statuses.APPROVED) &
			Q(date_time_of_rent_begin__lte=value.stop) & Q(
				date_time_of_rent_begin__gte=value.start) |
			Q(date_time_of_rent_end__gte=value.start) & Q(
				date_time_of_rent_end__lte=value.stop) |
			Q(date_time_of_rent_begin__gte=value.start) & Q(
				date_time_of_rent_end__lte=value.stop)
		).values_list('animal_id', flat=True)
		return queryset.exclude(id__in=free_animals_ids)
