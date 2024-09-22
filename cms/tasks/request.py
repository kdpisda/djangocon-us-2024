import logging

from tutorial.celery import app

logger = logging.getLogger(__name__)


@app.task()
def get_lyrics(request_id):
    logger.info(f"Finding Lyrics for Request ID: {request_id}")
    pass
