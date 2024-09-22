from auditlog.registry import auditlog

from cms.models.country import Country
from cms.models.gpt import GPTLog
from cms.models.musix import MusixLog
from cms.models.request import Request
from cms.models.song import Song

auditlog.register(Country)
auditlog.register(GPTLog)
auditlog.register(MusixLog)
auditlog.register(Request)
auditlog.register(Song)
