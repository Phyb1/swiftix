from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve as static_serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cart/", include("apps.cart.urls")),
    path("", include("apps.catalog.urls")),
    path("", include("apps.services.urls")),
    path("", include("apps.posters.urls")),
    path("", include("apps.core.urls")),
]

# Static/media are served here explicitly (not just via WhiteNoise) because this
# app is deployed under a Passenger sub-URI (e.g. mathxu.co.zw/onspot/). Passenger
# strips that sub-path into SCRIPT_NAME before Django ever sees the request, so
# WhiteNoise's simple "does PATH_INFO start with STATIC_URL" check can never match
# when STATIC_URL itself includes the sub-path prefix (needed for correct hrefs in
# the browser). Django's own URL resolver, unlike WhiteNoise, correctly matches
# against the already-SCRIPT_NAME-stripped PATH_INFO, so a plain "static/" /
# "media/" pattern here works regardless of what sub-path the app is mounted under.
#
# NOTE: this assumes STATIC_URL / MEDIA_URL always end in "static/" / "media/"
# (true for both root and sub-path deployments in this project's .env.example).
urlpatterns += [
    re_path(r"^static/(?P<path>.*)$", static_serve, {"document_root": settings.STATIC_ROOT}),
    re_path(r"^media/(?P<path>.*)$", static_serve, {"document_root": settings.MEDIA_ROOT}),
]
