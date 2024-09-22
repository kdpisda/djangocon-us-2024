from django.contrib import admin


class MusixLogAdmin(admin.ModelAdmin):
    list_display = ("id", "endpoint", "status_code")
    search_fields = ("endpoint", "status_code")
    list_filter = ("status_code", "endpoint")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
