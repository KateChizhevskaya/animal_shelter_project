from django.db import IntegrityError, connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from animal_rent_api.apps.additional_documents.models import Portfolio
from animal_rent_api.apps.additional_documents.serializers import PortfolioSerializer
from animal_rent_api.apps.animals.constants import DANGEROUS_BREEDS, ADD_ANIMAL_HEADER, ADD_ANIMAL_TEXT
from animal_rent_api.apps.animals.models import Animal
from animal_rent_api.apps.reactions.serializers import ReviewShowSerializer
from animal_rent_api.apps.requests.serializers import CreateAddAnimalForRentRequestSerializer
from animal_rent_api.apps.services.email_services.message_sender import EmailSender
from animal_rent_api.apps.user.constants import UserRoleEnum
from animal_rent_api.apps.user.services import get_admins


class AnimalListSerializer(ModelSerializer):
	class Meta:
		model = Animal
		fields = [
			'id',
			'animal_name',
			'description'
		]


class AnimalCreateSerializer(ModelSerializer):
	portfolio = PortfolioSerializer(required=False)

	class Meta:
		model = Animal
		fields = [
			'id',
			'animal_name',
			'description',
			'portfolio',
			'animal_type',
			'breed',
			'height',
			'weight',
			'delivery_type',
			'price',
			'price_for_business'
		]
		extra_kwargs = {
			'animal_name': {
				'min_length': 3,
				'max_length': 100,
				'required': False,
			},
			'animal_type': {
				'required': True,
				'allow_null': False
			},
			'breed': {
				'min_length': 3,
				'max_length': 100,
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
			'height': {
				'required': True
			},
			'weight': {
				'required': True,
				'allow_null': False
			},
			'delivery_type': {
				'required': False,
			},
			'description': {
				'required': False,
			},
			'price': {
				'required': True
			},
			'price_for_business': {
				'required': True
			},
		}

	def _validate_breed(self, attrs):
		if attrs.get('breed') in DANGEROUS_BREEDS:
			raise serializers.ValidationError(
				'This breed is dangerous'
			)

	def validate(self, attrs):
		self._validate_breed(attrs)
		return attrs

	def _create_animal(self, validated_data):
		with connection.cursor() as cursor:
			portfolio = validated_data.pop('portfolio')
			owner = self.context['request'].user
			cursor.execute(
				"INSERT INTO apps_portfolio (additional_description, awards, past_photo_places) VALUES ( %s, %s, %s ) returning id",
				(portfolio["additional_description"], portfolio["awards"], portfolio["past_photo_places"],))
			portfolio_id = cursor.fetchone()[0]
			cursor.execute(
				'''SELECT apps_animal.id FROM apps_animal WHERE
				apps_animal.animal_type = %s AND
				apps_animal.breed = %s AND
				apps_animal.owner_id = %s AND
				apps_animal.animal_name = %s''',
				(
					validated_data['animal_type'], validated_data['breed'], self.context['request'].user.id,
					validated_data['animal_name']
				)
			)
			existed_animal = cursor.fetchone()
			if existed_animal:
				animal_id = existed_animal[0]
				cursor.execute(
					'''UPDATE apps_animal SET description = %s, 
					portfolio_id = %s, height = %s, weight = %s,
					delivery_type = %s, price = %s,
					price_for_business = %s WHERE id = %s returning id''',
					(
						validated_data.get('description'), portfolio_id, validated_data.get('height'),
						validated_data.get('weight'), validated_data.get('delivery_type'), validated_data.get('price'),
						validated_data.get('price_for_business'), animal_id
					)
				)
			else:
				cursor.execute(
					'''INSERT INTO apps_animal(animal_name, description, portfolio_id, animal_type, breed, height, weight,
					delivery_type, price, price_for_business, rating, blocked, owner_id) VALUES (
					%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id''',
					(
						validated_data.get('animal_name'), validated_data.get('description'), portfolio_id,
						validated_data.get('animal_type'),
						validated_data.get('breed'), validated_data.get('height'), validated_data.get('weight'),
						validated_data.get('delivery_type'),
						validated_data.get('price'), validated_data.get('price_for_business'), validated_data.get('rating', 0),
						'true', owner.id
					)
				)
				animal_id = cursor.fetchone()[0]
		return animal_id, owner.id

	def _create_request(self, animal, owner):
		request_serialiazer = CreateAddAnimalForRentRequestSerializer(data={
			'lessor': owner,
			'animal': animal
		})
		try:
			request_serialiazer.is_valid(raise_exception=True)
		except Exception:
			raise serializers.ValidationError(
				'Can not create request'
			)
		request_serialiazer.save()
		admins = get_admins()
		EmailSender.send_mails_to_many_users(header=ADD_ANIMAL_HEADER, text=ADD_ANIMAL_TEXT, users=admins)

	def save(self):
		validated_data = self.validated_data
		animal, owner = self._create_animal(validated_data)
		self._create_request(animal, owner)


class RetrieveAnimalSerializer(ModelSerializer):
	portfolio = PortfolioSerializer(read_only=True)
	reviews = ReviewShowSerializer(read_only=True, many=True)

	class Meta:
		model = Animal
		fields = [
			'id',
			'animal_name',
			'description',
			'portfolio',
			'breed',
			'height',
			'weight',
			'delivery_type',
			'price',
			'price_for_business',
			'reviews'
		]

	def to_representation(self, instance):
		representation_result = super(RetrieveAnimalSerializer, self).to_representation(instance)
		if self.context['request'].user and self.context['request'].user.role == UserRoleEnum.ENTITY:
			representation_result.pop('price')
			representation_result.pop('description')
		else:
			representation_result.pop('portfolio')
			representation_result.pop('price_for_business')
		return representation_result
