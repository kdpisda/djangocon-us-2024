from django.db import models

from utils.mixins.models.timestamps import TimeStampedModel


class Country(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Countries"
        verbose_name = "Country"

    def __str__(self):
        return self.name
