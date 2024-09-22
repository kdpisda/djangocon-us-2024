from django.contrib import admin

from cms.tasks import get_lyrics


class RequestAdmin(admin.ModelAdmin):
    list_display = ("artist", "track", "song", "user", "status")
    list_filter = ("status",)
    search_fields = ("artist", "track", "user__username")
    autocomplete_fields = ("song", "user")

    def get_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return super().get_fields(request, obj)
        return ("artist", "track")  # fields shown on the add form

    def fetch_lyrics(self, request, queryset):
        for obj in queryset:  # noqa
            get_lyrics.delay(obj.id)

    fetch_lyrics.short_description = "Fetch Lyrics for selected requests"
    actions = [fetch_lyrics]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
