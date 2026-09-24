import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_home_page_has_nav_toggle_button(client):
    response = client.get(reverse("core:home"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "data-nav-toggle" in content
    assert 'id="main-nav"' in content


def test_home_page_has_whatsapp_fab_linking_to_order_number(client, settings):
    response = client.get(reverse("core:home"))
    content = response.content.decode()

    assert 'class="whatsapp-fab"' in content
    assert f"https://wa.me/{settings.WHATSAPP_ORDER_NUMBER}" in content
