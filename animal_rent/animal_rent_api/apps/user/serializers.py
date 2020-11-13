from django.db import connection
from rest_framework.serializers import ModelSerializer

from django.contrib.auth import authenticate, login
from rest_framework import serializers
from animal_rent_api.apps.services.email_services.constants import REGISTRATION_HEADER, REGISTRATION_TEXT
from animal_rent_api.apps.services.email_services.message_sender import EmailSender
from animal_rent_api.apps.user.constants import UserRoleEnum
from animal_rent_api.apps.user.models import RentUser


class UpdateUserSerializer(ModelSerializer):
	repeated_new_password = serializers.CharField(
		min_length=3,
		max_length=100,
		required=True,
		allow_blank=False,
		allow_null=False,
		write_only=True
	)
	new_password = serializers.CharField(
		min_length=3,
		max_length=100,
		required=True,
		allow_blank=False,
		allow_null=False,
		write_only=True
	)

	class Meta:
		model = RentUser
		fields = [
			'password',
			'phone_number',
			'new_password',
			'repeated_new_password'
		]
		extra_kwargs = {
			'phone_number': {'required': False},
			'password': {
				'min_length': 3,
				'max_length': 100,
				'required': False,
				'allow_blank': False,
				'allow_null': False
			},
		}

	def _validate_password_change(self, attrs):
		new_password = attrs.get('new_password')
		if new_password:
			repeated_new_password = attrs.get('repeated_new_password')
			old_password = attrs.get('password')
			if repeated_new_password is None or old_password is None:
				raise serializers.ValidationError(
					'You have to provide old password and repeat new one'
				)
			if not self.instance.check_password(old_password):
				raise serializers.ValidationError(
					'You enter incorrect old password'
				)
			if repeated_new_password != new_password:
				raise serializers.ValidationError(
					'You passwords are different'
				)
			if new_password == old_password:
				raise serializers.ValidationError(
					'You old and new passwords are the same'
				)
			self.instance.set_password(new_password)
			self.instance.save()
			attrs.pop('new_password')
			attrs.pop('password')
			attrs.pop('repeated_new_password')

	def validate(self, attrs):
		self._validate_password_change(attrs)
		return attrs


class RegistrationSerializer(ModelSerializer):
	repeated_password = serializers.CharField(
		min_length=3,
		max_length=100,
		required=True,
		allow_blank=False,
		allow_null=False
	)

	class Meta:
		model = RentUser
		fields = [
			'email',
			'password',
			'phone_number',
			'first_name',
			'last_name',
			'repeated_password',
			'role',
		]
		extra_kwargs = {
			'role': {
				'required': False,
			},
			'phone_number': {'required': False},
			'first_name': {
				'min_length': 3,
				'max_length': 100,
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
			'last_name': {
				'min_length': 3,
				'max_length': 100,
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
			'password': {
				'min_length': 3,
				'max_length': 100,
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
			'email': {
				'min_length': 3,
				'max_length': 100,
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
		}

	def _validate_password(self, attrs):
		password = attrs.get('password')
		repeated_password = attrs.get('repeated_password')
		if password != repeated_password:
			raise serializers.ValidationError('Password and repeated password are not the same')

	def validate(self, attrs):
		if not attrs.get('username', None):
			attrs['username'] = attrs.get('email')
		self._validate_password(attrs)
		return attrs

	def _get_existed_user(self, email):
		with connection.cursor() as cursor:
			cursor.execute(
				'''SELECT apps_rentuser.id FROM apps_rentuser WHERE
				apps_rentuser.email = %s''',
				(
					email,
				)
			)
			return cursor.fetchone()

	def save(self):
		with connection.cursor() as cursor:
			existed_user = self._get_existed_user(self.validated_data['email'])
			if existed_user:
				raise serializers.ValidationError('That user already exists')
			RentUser.objects.create_user(
				username=self.validated_data['username'],
				email=self.validated_data['email'],
				password=self.validated_data['password'],
			)
			existed_user = self._get_existed_user(self.validated_data['email'])
			if self.validated_data.get('role'):
				role = self.validated_data.get('role')
			else:
				role = UserRoleEnum.INDIVIDUAL
			cursor.execute(
					'''UPDATE apps_rentuser SET first_name = %s, last_name = %s, phone_number = %s, role = %s WHERE id = %s returning *''',
					(
						self.validated_data['first_name'], self.validated_data['last_name'],
						self.validated_data.get('phone_number'), role, existed_user
					)
				)
			user = cursor.fetchone()
			EmailSender.send_email(REGISTRATION_HEADER, REGISTRATION_TEXT, {'email': user[4]})
			return user


class LoginSerializer(ModelSerializer):
	class Meta:
		model = RentUser
		fields = [
			'email',
			'password',
		]
		extra_kwargs = {
			'password': {
				'min_length': 3,
				'max_length': 100,
				'required': True,
				'allow_blank': False,
				'allow_null': False
			},
			'email': {
				'required': True,
				'allow_blank': False,
				'allow_null': False
			}
		}

	def save(self):
		user = authenticate(username=self.validated_data['email'], password=self.validated_data['password'])
		if user:
			login(request=self.context['view'].request, user=user)
			if user.is_deleted:
				raise serializers.ValidationError(
					'The password is valid, but the account has been disabled!'
				)
		else:
			raise serializers.ValidationError('The username or password were incorrect')
		return user


class UserListChangeStatusSerializer(ModelSerializer):
	class Meta:
		model = RentUser
		fields = [
			'id',
			'email',
			'is_deleted',
		]
		extra_kwargs = {
			'id': {
				'read_only': True
			},
			'email': {
				'read_only': True
			}
		}

