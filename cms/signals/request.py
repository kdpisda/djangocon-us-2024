import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from cms.models.request import Request


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Request)
def process_request(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Request ID: {instance.id} created initiating get_lyrics task")
        # TODO: add task to get lyrics
