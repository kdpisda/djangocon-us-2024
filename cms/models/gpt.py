from django.db import models

from utils.mixins.models.timestamps import TimeStampedModel


class GPTLog(TimeStampedModel, models.Model):
    model = models.CharField(max_length=255, help_text="Name of the model.")
    prompt = models.TextField(help_text="Prompt for the model.")
    response = models.TextField(help_text="Response from the model.")

    class Meta:
        verbose_name_plural = "GPT Logs"
        verbose_name = "GPT Log"
