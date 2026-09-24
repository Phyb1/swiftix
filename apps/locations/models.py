from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.http import urlencode


class Branch(models.Model):
    """A physical business location shown on the About page.

    Deliberately generic — no Swiftix-specific fields — so this whole app
    (model, admin, template tag, CSS) can be copied into other PHYB client
    projects as-is. Location is shown as an admin-uploaded static image
    (a screenshot from any maps app) rather than a live embedded map: two
    different free tile providers (OSM's demo server, CARTO's legacy
    basemaps) both turned out to block/gate exactly this kind of embedded
    production use, and a static image + a real directions link is more
    reliable than chasing a third free tier. Coordinates are still
    optional and, when present, make the directions link open a precise
    pin instead of a text-address search.
    """

    name = models.CharField(max_length=100, help_text="e.g. 'Harare branch'.")
    address = models.CharField(max_length=255)
    phone = models.CharField(
        max_length=30, blank=True,
        help_text="Optional. Leave blank to use the site's main phone number.",
    )
    whatsapp_number = models.CharField(
        max_length=20, blank=True,
        help_text=(
            "Optional, international format digits only (e.g. 263781332627). "
            "Leave blank to use the site's main WhatsApp number."
        ),
    )
    map_image = models.ImageField(
        upload_to="branches/", blank=True, null=True,
        help_text=(
            "Optional screenshot/photo showing this branch's location "
            "(e.g. a Google Maps screenshot). Leave blank to show just "
            "the directions button."
        ),
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text=(
            "Optional — makes the directions button open a precise pin "
            "instead of a text search. In Google Maps: long-press the "
            "exact spot on the map, then copy the first number shown at "
            "the bottom of the screen."
        ),
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Same long-press — copy the second number shown.",
    )
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    @property
    def has_coordinates(self):
        return self.latitude is not None and self.longitude is not None

    def get_directions_url(self):
        """Google Maps directions link. Uses the precise pin when we have
        coordinates, otherwise falls back to a text-address search so the
        link still works before anyone has filled in lat/lng."""
        destination = f"{self.latitude},{self.longitude}" if self.has_coordinates else self.address
        return "https://www.google.com/maps/dir/?" + urlencode({"api": "1", "destination": destination})
