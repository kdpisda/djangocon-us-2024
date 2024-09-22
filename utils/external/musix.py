import logging
import os

import requests

from cms.models.musix import MusixLog


class MusixMatchClient:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_key = os.getenv("MUSIXMATCH_API_KEY")
        self.base_url = "https://api.musixmatch.com/ws/1.1/"

    def log_request(self, endpoint, params, response, status_code):
        try:
            MusixLog.objects.create(
                endpoint=endpoint,
                params=params,
                response=response,
                status_code=status_code,
            )
            self.logger.info("Logged MusixMatch request")
        except Exception as err:
            self.logger.error(f"Error logging MusixMatch request: {err}")

    def get(self, url, params):
        url = f"{self.base_url}{url}"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        response = requests.get(url, params=params, headers=headers)
        self.logger.info(
            f"Request to {response.url} returned status code {response.status_code}"
        )
        self.log_request(url, params, response.json(), response.status_code)
        if response.status_code == 200:
            resp_json = response.json()
            return resp_json.get("message", {}).get("body", {})
        return None

    def get_track(self, artist_name, track_name):
        self.logger.info(
            f"Getting track for artist: {artist_name}, track: {track_name}"
        )
        url = "matcher.track.get"
        params = {
            "q_artist": artist_name,
            "q_track": track_name,
            "apikey": self.api_key,
            "format": "json",
        }
        return self.get(url, params=params)

    def get_lyrics(self, artist_name, track_name):
        self.logger.info(
            f"Getting lyrics for artist: {artist_name}, track: {track_name}"
        )
        url = "matcher.lyrics.get"
        params = {
            "q_artist": artist_name,
            "q_track": track_name,
            "apikey": self.api_key,
            "format": "json",
        }
        return self.get(url, params=params)
