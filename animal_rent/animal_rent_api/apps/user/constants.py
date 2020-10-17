from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoleEnum(models.TextChoices):
	ENTITY = 'entity', _('Entity')
	INDIVIDUAL = 'individual', _('Individual')
