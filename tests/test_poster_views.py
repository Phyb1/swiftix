import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_poster_list_shows_only_active_posters(client, poster, inactive_poster):
    response = client.get(reverse("posters:poster_list"))
    assert response.status_code == 200
    posters = response.context["posters"]
    assert poster in posters
    assert inactive_poster not in posters


def test_poster_list_orders_newest_first(client, poster, db):
    from apps.posters.models import Poster

    older = Poster.objects.create(
        caption="Older promo", posted_date="2026-01-01", is_active=True
    )
    response = client.get(reverse("posters:poster_list"))
    posters = list(response.context["posters"])
    assert posters.index(poster) < posters.index(older)


def test_poster_list_renders_without_image_attached(client, poster):
    # Regression test: a poster with no image file must render the
    # placeholder rather than raising in the template.
    response = client.get(reverse("posters:poster_list"))
    assert response.status_code == 200
    assert b"poster-placeholder.png" in response.content


def test_poster_list_empty_state(client):
    response = client.get(reverse("posters:poster_list"))
    assert response.status_code == 200
    assert list(response.context["posters"]) == []
