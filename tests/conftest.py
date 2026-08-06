import pytest

from apps.catalog.models import Category, Product
from apps.posters.models import Poster
from apps.services.models import Service


@pytest.fixture
def category(db):
    return Category.objects.create(name="Computer Boxes", order=1)


@pytest.fixture
def out_of_stock_category(db):
    return Category.objects.create(name="Gearboxes", order=2)


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        category=category,
        name="Honda Fit Hybrid ECU Computer Box",
        price="180.00",
        in_stock=True,
        is_featured=True,
    )


@pytest.fixture
def poa_product(db, category):
    return Product.objects.create(
        category=category,
        name="Toyota Aqua Hybrid Battery Module",
        price=None,
        in_stock=True,
    )


@pytest.fixture
def out_of_stock_product(db, category):
    return Product.objects.create(
        category=category,
        name="Sold Out Gearbox Unit",
        price="450.00",
        in_stock=False,
    )


@pytest.fixture
def service(db):
    return Service.objects.create(
        name="Hybrid Battery Service",
        short_description="Inspection, repair & reconditioning for hybrid battery packs.",
        is_active=True,
        order=1,
    )


@pytest.fixture
def inactive_service(db):
    return Service.objects.create(
        name="Discontinued Service",
        is_active=False,
        order=2,
    )


@pytest.fixture
def poster(db):
    return Poster.objects.create(
        caption="Genuine hybrid spare parts — in stock now",
        posted_date="2026-07-04",
        is_active=True,
    )


@pytest.fixture
def inactive_poster(db):
    return Poster.objects.create(
        caption="Expired promo",
        posted_date="2026-01-01",
        is_active=False,
    )
