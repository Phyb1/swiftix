import io
import os

from django.core.files.base import ContentFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.http import urlencode
from PIL import Image

# Uploaded map_image files are downscaled/re-encoded to keep page weight
# reasonable for visitors on mobile data.
MAP_IMAGE_MAX_WIDTH = 1400
MAP_IMAGE_QUALITY = 85


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
            "(e.g. a Google Maps screenshot). Automatically resized/"
            "compressed on upload. Leave blank to show just the "
            "directions button."
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

    def save(self, *args, **kwargs):
        # `_committed` is False only for a file newly assigned this save
        # (a fresh upload) — an already-stored file being re-saved because
        # some other field changed has `_committed=True` and is left
        # alone, so editing e.g. the phone number doesn't silently
        # re-compress (and re-degrade) the image on every admin save.
        if self.map_image and not self.map_image._committed:
            self.map_image = self._compressed_map_image()
        super().save(*args, **kwargs)

    def _compressed_map_image(self):
        """Downscale to MAP_IMAGE_MAX_WIDTH and re-encode as JPEG so a
        full-resolution phone screenshot doesn't ship to every visitor at
        full size — the card only ever displays this at a few hundred px
        wide anyway."""
        image = Image.open(self.map_image)
        image = image.convert("RGB")  # JPEG has no alpha channel
        if image.width > MAP_IMAGE_MAX_WIDTH:
            ratio = MAP_IMAGE_MAX_WIDTH / float(image.width)
            new_height = round(image.height * ratio)
            image = image.resize((MAP_IMAGE_MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=MAP_IMAGE_QUALITY, optimize=True)
        new_name = os.path.splitext(self.map_image.name)[0] + ".jpg"
        return ContentFile(buffer.getvalue(), name=new_name)
