from django.contrib import admin

from .models import Poster


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = ("caption", "posted_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("caption",)
    date_hierarchy = "posted_date"
    ordering = ("-posted_date",)
