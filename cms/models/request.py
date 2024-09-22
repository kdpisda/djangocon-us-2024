from django.contrib.auth import get_user_model
from django.db import models

from utils.mixins.models.timestamps import TimeStampedModel

User = get_user_model()


class RequestStatus(models.TextChoices):
    INITIALIZED = "INITIALIZED", "Initialized"
    PROCESSING = "PROCESSING", "Processing"
    SONG_FOUND = "SONG_FOUND", "Song Found"
    LYRICS_FOUND = "LYRICS_FOUND", "Lyrics Found"
    SUMMARY_GENERATED = "SUMMARY_GENERATED", "Summary Generated"
    COMPLETED = "COMPLETED", "Completed"
    NOT_FOUND = "NOT_FOUND", "Not Found"
    FAILED = "FAILED", "Failed"


class Request(TimeStampedModel, models.Model):
    artist = models.CharField(max_length=255, help_text="Name of the artist.")
    track = models.CharField(max_length=255, help_text="Name of the track.")
    song = models.ForeignKey(
        "Song", on_delete=models.SET_NULL, null=True, help_text="Reference to the song."
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Request made by the user.",
    )
    status = models.CharField(
        choices=RequestStatus.choices,
        default=RequestStatus.INITIALIZED,
        max_length=255,
        help_text="Status of the request.",
    )
    errors = models.TextField(
        null=True, blank=True, help_text="Errors encountered during processing."
    )

    def __str__(self):
        return f"{self.track} by {self.artist}"
