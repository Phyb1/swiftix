import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_cart_add_redirects_and_stores_item(client, product):
    url = reverse("cart:cart_add", kwargs={"product_id": product.id})
    response = client.post(url, {"quantity": 2})
    assert response.status_code == 302
    session = client.session
    assert session["cart"][str(product.id)]["quantity"] == 2


def test_cart_add_rejects_out_of_stock(client, out_of_stock_product):
    url = reverse("cart:cart_add", kwargs={"product_id": out_of_stock_product.id})
    response = client.post(url, {"quantity": 1})
    assert response.status_code == 404


def test_cart_add_rejects_poa_product(client, poa_product):
    # POA items have no fixed price, so they must never enter the cart.
    url = reverse("cart:cart_add", kwargs={"product_id": poa_product.id})
    response = client.post(url, {"quantity": 1})
    assert response.status_code == 302
    assert client.session.get("cart", {}) == {}


def test_cart_detail_generates_whatsapp_link(client, product, settings):
    settings.WHATSAPP_ORDER_NUMBER = "263781332627"
    add_url = reverse("cart:cart_add", kwargs={"product_id": product.id})
    client.post(add_url, {"quantity": 1})

    response = client.get(reverse("cart:cart_detail"))
    assert response.status_code == 200
    link = response.context["whatsapp_link"]
    assert link.startswith("https://wa.me/263781332627?text=")
    assert "Honda" in link or "Honda%20" in link


def test_cart_detail_empty_has_no_whatsapp_link(client):
    response = client.get(reverse("cart:cart_detail"))
    assert response.context["whatsapp_link"] is None


def test_cart_remove(client, product):
    add_url = reverse("cart:cart_add", kwargs={"product_id": product.id})
    client.post(add_url, {"quantity": 1})

    remove_url = reverse("cart:cart_remove", kwargs={"product_id": product.id})
    response = client.post(remove_url)
    assert response.status_code == 302
    assert client.session["cart"] == {}


# --- Error handling regression tests ---

def test_cart_add_with_non_numeric_quantity_falls_back_to_one(client, product):
    # Regression test: a tampered/broken form value must not 500 the page.
    url = reverse("cart:cart_add", kwargs={"product_id": product.id})
    response = client.post(url, {"quantity": "not-a-number"})
    assert response.status_code == 302
    assert client.session["cart"][str(product.id)]["quantity"] == 1


def test_cart_add_with_missing_quantity_defaults_to_one(client, product):
    url = reverse("cart:cart_add", kwargs={"product_id": product.id})
    response = client.post(url, {})
    assert response.status_code == 302
    assert client.session["cart"][str(product.id)]["quantity"] == 1


def test_cart_add_clamps_absurd_quantity(client, product):
    url = reverse("cart:cart_add", kwargs={"product_id": product.id})
    client.post(url, {"quantity": "99999999"})
    assert client.session["cart"][str(product.id)]["quantity"] == 999


def test_cart_add_clamps_negative_quantity_to_minimum(client, product):
    url = reverse("cart:cart_add", kwargs={"product_id": product.id})
    client.post(url, {"quantity": "-5"})
    assert client.session["cart"][str(product.id)]["quantity"] == 1


def test_cart_add_ignores_external_next_url(client, product):
    # Regression test: an open-redirect attempt via `next` must be ignored,
    # falling back to the cart detail page instead of following it.
    url = reverse("cart:cart_add", kwargs={"product_id": product.id})
    response = client.post(url, {"quantity": 1, "next": "https://evil.example.com/phish"})
    assert response.status_code == 302
    assert response.url == reverse("cart:cart_detail")


def test_cart_add_follows_safe_same_site_next_url(client, product):
    url = reverse("cart:cart_add", kwargs={"product_id": product.id})
    target = reverse("catalog:product_detail", kwargs={"slug": product.slug})
    response = client.post(url, {"quantity": 1, "next": target})
    assert response.status_code == 302
    assert response.url == target
