from django.contrib import admin

from .models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "pinned_on_map", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "address")
    fields = (
        "name", "address", "phone", "whatsapp_number",
        "latitude", "longitude", "order", "is_active",
    )

    @admin.display(boolean=True, description="Pinned on map")
    def pinned_on_map(self, obj):
        return obj.has_coordinates
