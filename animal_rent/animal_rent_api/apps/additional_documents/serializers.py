from rest_framework.serializers import ModelSerializer

from animal_rent_api.apps.additional_documents.models import Portfolio


class PortfolioSerializer(ModelSerializer):

	class Meta:
		model = Portfolio
		fields = '__all__'
		extra_kwargs = {
			'awards': {
				'required': False,
			},
			'past_photo_places': {
				'required': False,
			},
			'additional_description': {
				'required': False,
			}
		}

