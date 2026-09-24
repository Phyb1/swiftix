from django.contrib import admin

from .models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "has_map_image", "has_coordinates", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "address")
    fields = (
        "name", "address", "phone", "whatsapp_number", "map_image",
        "latitude", "longitude", "order", "is_active",
    )

    @admin.display(boolean=True, description="Has image")
    def has_map_image(self, obj):
        return bool(obj.map_image)

    @admin.display(boolean=True, description="Precise directions")
    def has_coordinates(self, obj):
        return obj.has_coordinates
