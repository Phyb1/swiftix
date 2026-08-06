from django.db import models
from django.urls import reverse


class Poster(models.Model):
    """A marketing poster/promo image the client can upload from admin,
    shown newest-first on the public Promotions gallery page."""

    caption = models.CharField(
        max_length=200,
        help_text="Short caption shown under the poster, e.g. the promo headline.",
    )
    image = models.ImageField(upload_to="posters/")
    posted_date = models.DateField(
        help_text="Date this poster/promo is for — controls display order.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide without deleting (e.g. an expired promo).",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-posted_date", "-created_at"]

    def __str__(self):
        return f"{self.caption} ({self.posted_date})"

    def get_absolute_url(self):
        return reverse("posters:poster_list")

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        return "/static/images/placeholders/poster-placeholder.png"
