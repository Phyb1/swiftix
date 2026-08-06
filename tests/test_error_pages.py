import pytest
from django.test import RequestFactory
from django.views.defaults import server_error

pytestmark = pytest.mark.django_db


def test_custom_404_page_renders(client, settings):
    # Django only uses templates/404.html when DEBUG=False — with DEBUG=True
    # it shows the technical debug page instead, which would make this test
    # pass even if our custom template were broken.
    settings.DEBUG = False
    settings.ALLOWED_HOSTS = ["testserver"]

    response = client.get("/this-page-does-not-exist/")

    assert response.status_code == 404
    content = response.content.decode()
    assert "404" in content
    assert "Back to home" in content


def test_custom_404_page_offers_whatsapp_fallback(client, settings):
    settings.DEBUG = False
    settings.ALLOWED_HOSTS = ["testserver"]
    settings.WHATSAPP_ORDER_NUMBER = "263781332627"

    response = client.get("/this-page-does-not-exist/")

    assert b"wa.me/263781332627" in response.content


def test_custom_500_page_renders_standalone():
    # The 500 handler is called directly (matching how Django's own error
    # machinery invokes it) since it intentionally receives no context —
    # this proves the template doesn't depend on context processors, which
    # matters because a 500 can happen precisely when those are broken.
    request = RequestFactory().get("/")
    response = server_error(request)

    assert response.status_code == 500
    content = response.content.decode()
    assert "500" in content
    assert "Back to home" in content
    assert "WhatsApp" in content
