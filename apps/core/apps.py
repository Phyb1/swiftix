from django.contrib import admin
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        admin.site.site_header = "Swiftix Auto Admin"
        admin.site.site_title = "Swiftix Auto Admin"
        admin.site.index_title = "Manage parts, services & promotions"
