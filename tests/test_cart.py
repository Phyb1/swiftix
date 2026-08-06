from decimal import Decimal

import pytest
from django.test import RequestFactory

from apps.cart.cart import CART_SESSION_KEY, Cart

pytestmark = pytest.mark.django_db


def _cart_with_session():
    request = RequestFactory().get("/")
    from django.contrib.sessions.middleware import SessionMiddleware

    SessionMiddleware(lambda r: None).process_request(request)
    request.session.save()
    return Cart(request)


def test_add_product_increments_quantity(product):
    cart = _cart_with_session()
    cart.add(product)
    cart.add(product)
    assert len(cart) == 2


def test_add_product_with_explicit_quantity(product):
    cart = _cart_with_session()
    cart.add(product, quantity=3)
    assert len(cart) == 3


def test_update_quantity(product):
    cart = _cart_with_session()
    cart.add(product)
    cart.update_quantity(product, 5)
    assert len(cart) == 5


def test_update_quantity_to_zero_removes_item(product):
    cart = _cart_with_session()
    cart.add(product)
    cart.update_quantity(product, 0)
    assert len(cart) == 0


def test_remove_product(product):
    cart = _cart_with_session()
    cart.add(product)
    cart.remove(product)
    assert len(cart) == 0


def test_get_total_price(product):
    cart = _cart_with_session()
    cart.add(product, quantity=2)
    expected = Decimal(str(product.price)) * 2
    assert cart.get_total_price() == expected


def test_iter_yields_product_and_subtotal(product):
    cart = _cart_with_session()
    cart.add(product, quantity=2)
    items = list(cart)
    assert len(items) == 1
    assert items[0]["product"] == product
    expected = Decimal(str(product.price)) * 2
    assert items[0]["subtotal"] == expected


def test_clear_empties_cart(product):
    cart = _cart_with_session()
    cart.add(product)
    cart.clear()
    assert len(cart) == 0


def test_clear_empties_underlying_session_not_just_stale_reference(product):
    # Regression test: clear() must update self.cart itself, not only
    # self.session[CART_SESSION_KEY], or len()/iteration keep seeing
    # the old in-memory dict.
    cart = _cart_with_session()
    cart.add(product, quantity=3)
    cart.clear()
    assert cart.cart == {}
    assert list(cart) == []
    assert cart.session[CART_SESSION_KEY] == {}
