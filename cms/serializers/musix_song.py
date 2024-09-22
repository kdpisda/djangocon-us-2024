from rest_framework import serializers

from cms.models.song import Song


class MusixSongSerializer(serializers.ModelSerializer):
    track_id = serializers.CharField(source="id", allow_null=False, allow_blank=False)
    track_name = serializers.CharField(
        source="name", allow_null=False, allow_blank=False
    )
    track_rating = serializers.CharField(
        source="rating", allow_null=False, allow_blank=False
    )
    explicit = serializers.CharField(allow_null=False, allow_blank=False)
    has_lyrics = serializers.CharField(allow_null=False, allow_blank=False)
    has_subtitles = serializers.CharField(allow_null=False, allow_blank=False)
    album_id = serializers.CharField(allow_null=False, allow_blank=False)
    album_name = serializers.CharField(allow_null=False, allow_blank=False)
    artist_id = serializers.CharField(allow_null=False, allow_blank=False)
    artist_name = serializers.CharField(allow_null=False, allow_blank=False)

    class Meta:
        model = Song
        fields = [
            "track_id",
            "track_name",
            "track_rating",
            "explicit",
            "has_lyrics",
            "has_subtitles",
            "album_id",
            "album_name",
            "artist_id",
            "artist_name",
        ]
