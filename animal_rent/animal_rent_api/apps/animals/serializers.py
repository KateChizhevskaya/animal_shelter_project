from django.db import IntegrityError
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
		portfolio = Portfolio.objects.create(**validated_data.pop('portfolio'))
		owner = self.context['request'].user
		validated_data['owner'] = owner
		try:
			animal, is_created = Animal.objects.filter(blocked=True).get_or_create(
				animal_type=validated_data['animal_type'],
				breed=validated_data['breed'],
				owner=validated_data['owner'],
				animal_name=validated_data['animal_name'],
				defaults=validated_data
			)
		except IntegrityError:
			raise serializers.ValidationError(
				'This animal already exists'
			)
		if not is_created:
			animal.photos = validated_data.get('photos')
			animal.description = validated_data.get('description')
			animal.height = validated_data.get('height')
			animal.weight = validated_data.get('weight')
			animal.delivery_type = validated_data.get('delivery_type')
			animal.price = validated_data.get('price')
			animal.price_for_business = validated_data.get('price_for_business')
			animal.portfolio = portfolio
		animal.save()
		return animal, owner

	def _create_request(self, animal, owner):
		request_serialiazer = CreateAddAnimalForRentRequestSerializer(data={
			'lessor': owner.id,
			'animal': animal.id
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
