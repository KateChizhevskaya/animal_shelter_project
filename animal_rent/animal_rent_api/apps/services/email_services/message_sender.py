from django.core.mail import send_mail

from animal_rent_api.apps.services.email_services.constants import SITE_EMAIL
from animal_rent_api.apps.user.models import RentUser


class EmailSender:
	@staticmethod
	def send_email(header, text, user):
		if isinstance(user, RentUser):
			email = user.email
		else:
			email = user['email']
		send_mail(header, text, SITE_EMAIL, (email, ), fail_silently=False)

	@staticmethod
	def send_mails_to_many_users(header, text, users):
		users_mails = (user.email for user in users)
		send_mail(header, text, SITE_EMAIL, users_mails, fail_silently=False)
