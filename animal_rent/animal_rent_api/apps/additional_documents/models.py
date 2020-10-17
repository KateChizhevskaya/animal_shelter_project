from django.db import models


class Portfolio(models.Model):
	additional_description = models.TextField(
		max_length=500,
		blank=True,
		null=True
	)
	awards = models.CharField(
		max_length=30,
		blank=True,
		null=True
	)
	past_photo_places = models.CharField(
		max_length=30,
		blank=True,
		null=True
	)
