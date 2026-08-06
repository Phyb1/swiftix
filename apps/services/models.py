from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Service(models.Model):
    """A quote-based offering, e.g. AC Installation, Fridge Repair.
    No price shown — customers request a quote via WhatsApp instead."""

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    short_description = models.CharField(
        max_length=200, blank=True,
        help_text="One-line summary shown on cards/home page.",
    )
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="services/", blank=True, null=True,
        help_text="Leave blank to use a placeholder image.",
    )
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("services:service_detail", kwargs={"slug": self.slug})

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        return "/static/images/placeholders/service-placeholder.png"
