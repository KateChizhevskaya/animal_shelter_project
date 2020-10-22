import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


class Statuses(models.TextChoices):
	IN_PROCESS = 'in_process', _('In process')
	APPROVED = 'approved', _('Approved')
	REJECTED = 'rejected', _('Rejected')


NOT_ACTIVE_STATUS = {Statuses.APPROVED, Statuses.REJECTED}

DEFAULT_MAIL_MESSAGES_FOR_ANSWER_REQUESTS = {
	Statuses.APPROVED: 'Сongratulations your request was approved!',
	Statuses.REJECTED: 'Your request was rejected, please contact with administrators to know the reason or try again'
}
ANSWER_REQUEST_HEADER = 'Your request was reviewed'

MAXiMUM_PERIOD_OF_ANIMAL_KEEPIND = datetime.timedelta(hours=6)

RENT_REQUEST_HEADER = 'You have new rent request'

RENT_REQUEST_TEXT = 'Please, react to new rent request'
