from django.contrib import admin

from cms.admin.gpt import GPTLogAdmin
from cms.admin.musix import MusixLogAdmin
from cms.admin.request import RequestAdmin
from cms.admin.song import SongAdmin
from cms.models.country import Country
from cms.models.gpt import GPTLog
from cms.models.musix import MusixLog
from cms.models.request import Request
from cms.models.song import Song


admin.site.register(Country)
admin.site.register(Request, RequestAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(GPTLog, GPTLogAdmin)
admin.site.register(MusixLog, MusixLogAdmin)
