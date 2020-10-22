from django.db import connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from animal_rent_api.apps.animals.models import Animal
from animal_rent_api.apps.reactions.models import Review, Complaint
from animal_rent_api.apps.requests.constants import Statuses
from animal_rent_api.apps.user.models import RentUser


class ReviewShowSerializer(ModelSerializer):
	class Meta:
		model = Review
		fields = [
			'id',
			'user',
			'rating',
			'text',
		]


class AddReviewSerializer(ModelSerializer):
	animal = serializers.PrimaryKeyRelatedField(queryset=Animal.objects.filter(blocked=False))

	class Meta:
		model = Review
		fields = [
			'id',
			'user',
			'rating',
			'text',
			'animal',
		]
		extra_kwargs = {
			'user': {
				'required': False,
			},
			'text': {
				'required': False,
			},
			'animal': {
				'required': True,
			},
			'rating': {
				'required': False
			}
		}

	def _validate_together(self, attrs):
		if attrs.get('text') is None and attrs.get('rating') is None:
			raise serializers.ValidationError(
				'You have to implement text or rating'
			)

	def _validate_rating(self, attrs):
		rating = attrs.get('rating')
		if rating is not None and (rating > 5 or rating < 0):
			raise serializers.ValidationError(
				'Rating can be from 0 to 5'
			)

	def _validate_animal(self, attr):
		animal = attr.get('animal')
		user = self.context['request'].user
		with connection.cursor() as cursor:
			cursor.execute(
				'''SELECT * from apps_rentrequest where status = %s AND animal_id = %s AND renter_id = %s''',
				(
					Statuses.APPROVED, animal.id, user.id
				)
			)
			existed_rent_request = cursor.fetchone()
		if not existed_rent_request:
			raise serializers.ValidationError(
				'You can not add comment to animal, that you have not rent yet'
			)

	def _add_user(self, attrs):
		user = self.context['request'].user
		attrs['user'] = user

	def validate(self, attrs):
		self._validate_together(attrs)
		self._validate_rating(attrs)
		self._validate_animal(attrs)
		self._add_user(attrs)
		return attrs

	def recalculate_animal_raiting(self, instance):
		animal = instance.animal
		with connection.cursor() as cursor:
			cursor.execute(
				'''SELECT rating from apps_review where animal_id = %s''',
				(
					animal.id,
				)
			)
			animal_reviews = [item[0] for item in cursor.fetchall()]
			new_rating = sum(map(lambda str_num: int(str_num), animal_reviews)) / len(animal_reviews)
			cursor.execute(
					'''UPDATE apps_animal SET rating = %s WHERE id = %s''',
					(
						new_rating, animal.id
					)
				)

	def create(self, validated_data):
		instance = super(AddReviewSerializer, self).create(validated_data)
		self.recalculate_animal_raiting(instance)
		return instance


class AddComplaintSerializer(ModelSerializer):
	defendant = serializers.PrimaryKeyRelatedField(queryset=RentUser.objects.filter(is_deleted=False))

	class Meta:
		model = Complaint
		fields = [
			'id',
			'complaint_creater',
			'defendant',
			'text'
		]
		extra_kwargs = {
			'complaint_creater': {
				'required': False,
			},
			'text': {
				'required': True,
			},
			'defendant': {
				'required': True,
			}
		}

	def validate(self, attrs):
		user = self.context['request'].user
		attrs['complaint_creater'] = user
		return attrs
