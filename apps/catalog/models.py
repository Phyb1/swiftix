from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Flat top-level category, e.g. Men, Women, Kids, Accessories."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:category_detail", kwargs={"slug": self.slug})


class Product(models.Model):
    """A single standalone listing (no size/colour variants)."""

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        help_text="Leave blank for 'Price on ask' items.",
    )
    image = models.ImageField(
        upload_to="products/", blank=True, null=True,
        help_text="Leave blank to use a placeholder image.",
    )
    in_stock = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        return "/static/images/placeholders/product-placeholder.png"

    @property
    def is_poa(self):
        """True when this item has no listed price (Price On Ask)."""
        return self.price is None

    @property
    def display_price(self):
        return f"${self.price}" if self.price is not None else "POA"
