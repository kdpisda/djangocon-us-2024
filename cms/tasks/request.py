import logging

from django.contrib.postgres.search import TrigramSimilarity

from cms.models.country import Country
from cms.models.request import Request
from cms.models.request import RequestStatus
from cms.models.song import Song
from cms.models.song import SongStatus
from cms.serializers.musix_song import MusixSongSerializer
from tutorial.celery import app
from utils.external.musix import MusixMatchClient
from utils.external.openai import ChatGPTClient

logger = logging.getLogger("celery")


def update_status(obj, status, status_attr="status", id_attr="id"):
    setattr(obj, status_attr, status)
    obj.save()
    logger.info(
        f"{obj.__class__.__name__} ID: {getattr(obj, id_attr)} status updated to {status}"
    )


def create_or_update_song(song_body):
    serializer = MusixSongSerializer(data=song_body)
    serializer.is_valid(raise_exception=True)
    song_body = serializer.validated_data
    song_id = song_body["id"]
    song, created = Song.objects.update_or_create(id=song_id, defaults=song_body)
    return song


def bulk_create_countries(countries):
    return Country.objects.bulk_create([Country(name=country) for country in countries])


def upsert_countries(song, countries):
    existing_countries = Country.objects.filter(name__in=countries).values_list(
        "name", flat=True
    )
    new_countries = list(set(countries) - set(existing_countries))
    bulk_create_countries(new_countries)
    song.countries.set(Country.objects.filter(name__in=countries))
    update_status(song, SongStatus.COMPLETED)


def generate_summary_and_countries(song):
    gpt = ChatGPTClient()
    song.summary = gpt.get_song_summary(song.lyrics)
    update_status(song, SongStatus.SUMMARY_GENERATED)
    countries = gpt.get_countries(song.lyrics)
    upsert_countries(song, countries)


def get_track_and_lyrics(req):
    musix = MusixMatchClient()
    fetched_song = None
    queryset = (
        Song.objects.annotate(
            name_similarity=TrigramSimilarity("name", req.track),
            artist_similarity=TrigramSimilarity("artist_name", req.artist),
        )
        .filter(
            name_similarity__gt=0.6,  # Adjust threshold as needed
            artist_similarity__gt=0.6,  # Adjust threshold as needed
        )
        .order_by("-name_similarity", "-artist_similarity")
    )
    if queryset.exists():
        fetched_song = queryset.first()
    song_data = (
        MusixSongSerializer(fetched_song).data
        if fetched_song
        else musix.get_track(req.artist, req.track)["track"]
    )

    if song_data:
        song = create_or_update_song(song_data)
        req.song = song
        update_status(req, RequestStatus.SONG_FOUND, status_attr="status", id_attr="id")
        if not song.lyrics:
            lyrics = musix.get_lyrics(req.artist, req.track)
            if lyrics:
                song.lyrics = lyrics.get("lyrics", {}).get("lyrics_body", "")
                update_status(song, SongStatus.LYRICS_FETCHED)
                update_status(
                    req, RequestStatus.LYRICS_FOUND, status_attr="status", id_attr="id"
                )
                generate_summary_and_countries(song)
            else:
                update_status(
                    req, RequestStatus.NOT_FOUND, status_attr="status", id_attr="id"
                )
    else:
        update_status(req, RequestStatus.NOT_FOUND, status_attr="status", id_attr="id")


@app.task(queue="lyrics")
def get_lyrics(request_id):
    logger.info(f"Finding Lyrics for Request ID: {request_id}")
    try:
        req = (
            Request.objects.filter(id=request_id)
            .exclude(status=RequestStatus.PROCESSING)
            .first()
        )
        if req:
            req.errors = None
            update_status(
                req, RequestStatus.PROCESSING, status_attr="status", id_attr="id"
            )
            get_track_and_lyrics(req)
            update_status(
                req, RequestStatus.COMPLETED, status_attr="status", id_attr="id"
            )
        else:
            logger.info(
                f"Request ID: {request_id} not found or already processing/processed."
            )
    except Exception as err:
        logger.error(f"Error while processing Request ID: {request_id}: {err}")
        if req:
            req.error = str(err)
            update_status(req, RequestStatus.FAILED, status_attr="status", id_attr="id")
