from decimal import Decimal

import pytest

pytestmark = pytest.mark.django_db


def test_category_slug_auto_generated(category):
    assert category.slug == "computer-boxes"


def test_product_slug_auto_generated(product):
    assert product.slug == "honda-fit-hybrid-ecu-computer-box"


def test_product_get_absolute_url(product):
    assert product.get_absolute_url() == f"/shop/item/{product.slug}/"


def test_category_get_absolute_url(category):
    assert category.get_absolute_url() == f"/shop/category/{category.slug}/"


def test_product_display_image_falls_back_to_placeholder(product):
    assert product.image.name in (None, "")
    assert product.display_image_url == "/static/images/placeholders/product-placeholder.png"


def test_category_str_and_ordering(category, out_of_stock_category):
    from apps.catalog.models import Category

    names = list(Category.objects.values_list("name", flat=True))
    assert names == ["Computer Boxes", "Gearboxes"]  # ordered by `order` field
    assert str(category) == "Computer Boxes"


def test_product_with_price_is_not_poa(product):
    assert product.is_poa is False
    assert product.display_price == "$180.00"


def test_product_without_price_is_poa(poa_product):
    assert poa_product.is_poa is True
    assert poa_product.display_price == "POA"


def test_service_slug_auto_generated(service):
    assert service.slug == "hybrid-battery-service"


def test_service_get_absolute_url(service):
    assert service.get_absolute_url() == f"/services/{service.slug}/"


def test_service_display_image_falls_back_to_placeholder(service):
    assert service.display_image_url == "/static/images/placeholders/service-placeholder.png"


def test_service_str(service):
    assert str(service) == "Hybrid Battery Service"


def test_poster_display_image_falls_back_to_placeholder(poster):
    # Poster fixture doesn't attach a real file — this proves a poster
    # without an image renders safely instead of raising in the template.
    assert not poster.image
    assert poster.display_image_url == "/static/images/placeholders/poster-placeholder.png"


def test_poster_str_includes_date(poster):
    assert str(poster) == "Genuine hybrid spare parts — in stock now (2026-07-04)"


def test_poster_ordering_newest_first(poster, inactive_poster):
    from apps.posters.models import Poster

    dates = list(Poster.objects.values_list("posted_date", flat=True))
    assert dates == sorted(dates, reverse=True)
