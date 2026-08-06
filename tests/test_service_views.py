import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_service_list_shows_active_services(client, service, inactive_service):
    response = client.get(reverse("services:service_list"))
    assert response.status_code == 200
    services = response.context["services"]
    assert service in services
    assert inactive_service not in services


def test_service_detail_renders(client, service):
    url = reverse("services:service_detail", kwargs={"slug": service.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["service"] == service


def test_service_detail_generates_whatsapp_quote_link(client, service, settings):
    settings.WHATSAPP_ORDER_NUMBER = "263781332627"
    settings.SITE_NAME = "Swiftix Auto Hybrid & Programming Solutions"
    url = reverse("services:service_detail", kwargs={"slug": service.slug})
    response = client.get(url)
    link = response.context["whatsapp_link"]
    assert link.startswith("https://wa.me/263781332627?text=")
    assert "Hybrid" in link


def test_service_detail_falls_back_gracefully_when_whatsapp_number_unset(client, service, settings):
    # Regression test: a misconfigured/blank WHATSAPP_ORDER_NUMBER must not
    # 500 the page — it should render with a phone/email fallback instead.
    settings.WHATSAPP_ORDER_NUMBER = ""
    url = reverse("services:service_detail", kwargs={"slug": service.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["whatsapp_link"] is None
    assert response.context["BUSINESS_PHONE_DISPLAY"] in response.content.decode()


def test_inactive_service_detail_404s(client, inactive_service):
    url = reverse("services:service_detail", kwargs={"slug": inactive_service.slug})
    response = client.get(url)
    assert response.status_code == 404
