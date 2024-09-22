from django.db import models

from utils.mixins.models.timestamps import TimeStampedModel


class MusixLog(TimeStampedModel, models.Model):
    endpoint = models.TextField(help_text="Endpoint of the request.")
    params = models.JSONField(help_text="Parameters of the request.")
    response = models.JSONField(help_text="Response of the request.")
    status_code = models.IntegerField(help_text="Status code of the response.")
