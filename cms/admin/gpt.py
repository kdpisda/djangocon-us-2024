from django.contrib import admin


class GPTLogAdmin(admin.ModelAdmin):
    list_display = ("id", "model", "response")
    search_fields = ("model",)
    list_filter = ("model",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
