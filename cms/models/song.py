from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from utils.mixins.models.timestamps import TimeStampedModel


class SongStatus(models.TextChoices):
    INITIALIZED = "INITIALIZED", "Initialized"
    LYRICS_FETCHED = "LYRICS_FETCHED", "Lyrics Fetched"
    SUMMARY_GENERATED = "SUMMARY_GENERATED", "Summary Generated"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"


class Song(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, help_text="Name of the song.")
    artist_id = models.IntegerField(help_text="ID of the artist.")
    artist_name = models.CharField(max_length=255, help_text="Name of the artist.")
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Rating of the song.",
    )
    explicit = models.BooleanField(
        default=False, help_text="Indicates whether the song is explicit."
    )
    has_lyrics = models.BooleanField(
        default=False, help_text="Indicates whether the song has lyrics."
    )
    lyrics = models.TextField(help_text="Lyrics of the song.")
    has_subtitles = models.BooleanField(
        default=False, help_text="Indicates whether the song has subtitles."
    )
    album_id = models.IntegerField(help_text="ID of the album.")
    album_name = models.CharField(max_length=255, help_text="Name of the album.")

    summary = models.TextField(null=True, blank=True, help_text="Summary of the song.")

    status = models.CharField(
        choices=SongStatus.choices,
        default=SongStatus.INITIALIZED,
        max_length=255,
        help_text="Status of the song.",
    )

    countries = models.ManyToManyField(
        "Country", related_name="songs", help_text="Countries found in the song."
    )

    def __str__(self):
        return f"{self.name} by {self.artist_name}"
