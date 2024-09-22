from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.mixins.models.timestamps import TimeStampedModel


class GenderChoice(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"
    NO_DISCLOSE = "NO_DISCLOSE", "Prefer not to disclose"


class User(TimeStampedModel, AbstractUser, models.Model):
    gender = models.CharField(
        choices=GenderChoice.choices, max_length=15, default=GenderChoice.NO_DISCLOSE
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
