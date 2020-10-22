from django.db import connection
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from animal_rent_api.apps.animals.models import Animal
from animal_rent_api.apps.requests.constants import Statuses, DEFAULT_MAIL_MESSAGES_FOR_ANSWER_REQUESTS, \
	ANSWER_REQUEST_HEADER, \
	MAXiMUM_PERIOD_OF_ANIMAL_KEEPIND, RENT_REQUEST_HEADER, RENT_REQUEST_TEXT
from animal_rent_api.apps.requests.models import AddAnimalForRentRequest, RentRequest
from animal_rent_api.apps.services.email_services.message_sender import EmailSender


class CreateAddAnimalForRentRequestSerializer(ModelSerializer):
	class Meta:
		model = AddAnimalForRentRequest
		fields = [
			'id',
			'lessor',
			'animal',
		]


class AddAnimalForRentRequestViewSerializer(ModelSerializer):
	class Meta:
		model = AddAnimalForRentRequest
		fields = [
			'id',
			'animal',
			'text_comment',
			'lessor',
			'date_of_creating_request',
			'status'
		]


class RentRequestViewSerializer(ModelSerializer):
	class Meta:
		model = RentRequest
		fields = [
			'id',
			'animal',
			'date_time_of_rent_begin',
			'date_time_of_rent_end',
			'renter_text_comment',
			'phone_number',
			'date_of_creating_request',
			'renter',
			'status'
		]


class AnswerAddAnimalForRentRequestSerializer(ModelSerializer):
	class Meta:
		model = AddAnimalForRentRequest
		fields = [
			'status',
			'text_comment'
		]
		extra_kwargs = {
			'status': {
				'required': True,
			},
			'text_comment': {
				'required': False,
				'allow_blank': True,
				'allow_null': True
			},
		}

	def unlock_animal(self, animal):
		with connection.cursor() as cursor:
			cursor.execute(
				'''UPDATE apps_animal SET blocked = %s WHERE id = %s ''',
				(
					False, animal.id
				)
			)

	def send_email(self, text, user):
		EmailSender.send_email(header=ANSWER_REQUEST_HEADER, text=text, user=user)

	def save(self):
		validated_data = self.validated_data
		comment = validated_data.get('text_comment')
		status = validated_data.get('status')
		if status in {Statuses.APPROVED, Statuses.REJECTED}:
			instance = super(AnswerAddAnimalForRentRequestSerializer, self).save()
			mail_text = comment if comment else DEFAULT_MAIL_MESSAGES_FOR_ANSWER_REQUESTS[status]
			if status == Statuses.APPROVED:
				self.unlock_animal(instance.animal)
			self.send_email(mail_text, instance.lessor)
		else:
			raise serializers.ValidationError(
				'Can not react this way'
			)


class CreateRentAnimalRequestSerializer(ModelSerializer):
	date_time_of_rent_begin = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	date_time_of_rent_end = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
	animal = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.filter(blocked=False, owner__is_deleted=False))

	class Meta:
		model = RentRequest
		fields = [
			'id',
			'animal',
			'date_time_of_rent_begin',
			'date_time_of_rent_end',
			'renter_text_comment',
			'phone_number'
		]
		extra_kwargs = {
			'animal': {
				'required': True,
				'allow_null': False
			},
			'renter_text_comment': {
				'required': False,
				'allow_blank': True,
				'allow_null': True
			},
			'phone_number': {
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
			'date_time_of_rent_begin': {
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
			'date_time_of_rent_end': {
				'required': True,
				'allow_blank': False,
				'allow_null': False
			}
		}

	def _validate_time_period(self, date_time_of_rent_begin, date_time_of_rent_end, animal):
		if date_time_of_rent_begin + MAXiMUM_PERIOD_OF_ANIMAL_KEEPIND < date_time_of_rent_end:
			raise serializers.ValidationError(
				'You can not take animal for more than 6 hours'
			)

	def _validate_animal(self, animal):
		if animal.blocked:
			raise serializers.ValidationError(
				'You can not rent that animal'
			)

	def _validate_phone_number(self, attrs):
		if not attrs.get('phone_number'):
			attrs['phone_number'] = self.context['request'].user.phone_number

	def validate(self, attrs):
		self._validate_phone_number(attrs)
		self._validate_animal(attrs['animal'])
		self._validate_time_period(attrs['date_time_of_rent_begin'], attrs['date_time_of_rent_end'], attrs['animal'])
		attrs['renter_id'] = self.context['request'].user.id
		return attrs

	def save(self):
		super(CreateRentAnimalRequestSerializer, self).is_valid(raise_exception=True)
		instance = super(CreateRentAnimalRequestSerializer, self).save()
		EmailSender.send_email(header=RENT_REQUEST_HEADER, text=RENT_REQUEST_TEXT, user=instance.animal.owner)
		return instance


class AnswerForRentRequestSerializer(ModelSerializer):
	class Meta:
		model = RentRequest
		fields = [
			'id',
			'status',
		]
		extra_kwargs = {
			'status': {
				'required': True,
			}
		}

	def save(self):
		validated_data = self.validated_data
		status = validated_data.get('status')
		if status in {Statuses.APPROVED, Statuses.REJECTED}:
			super(AnswerForRentRequestSerializer, self).save()
		else:
			raise serializers.ValidationError(
				'Can not react this way'
			)
