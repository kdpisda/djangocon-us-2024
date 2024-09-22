from django.contrib import admin


class SongAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "artist_name",
        "rating",
        "explicit",
        "has_lyrics",
        "album_name",
        "status",
    )
    list_filter = ("explicit", "has_lyrics", "status")
    search_fields = ("name", "artist_name", "album_name")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
