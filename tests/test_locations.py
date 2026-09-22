import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_branch_str(branch_with_coordinates):
    assert str(branch_with_coordinates) == "Harare branch"


def test_branch_with_coordinates_has_coordinates_true(branch_with_coordinates):
    assert branch_with_coordinates.has_coordinates is True


def test_branch_without_coordinates_has_coordinates_false(branch_without_coordinates):
    assert branch_without_coordinates.has_coordinates is False


def test_directions_url_uses_lat_lng_when_available(branch_with_coordinates):
    url = branch_with_coordinates.get_directions_url()
    assert url.startswith("https://www.google.com/maps/dir/?")
    assert "destination=-17.858" in url
    assert "31.017" in url


def test_directions_url_falls_back_to_address(branch_without_coordinates):
    # No lat/lng yet — the link must still work, just via a text search
    # instead of a precise pin.
    url = branch_without_coordinates.get_directions_url()
    assert url.startswith("https://www.google.com/maps/dir/?")
    assert "Shamrock" in url


def test_branch_ordering(branch_without_coordinates, branch_with_coordinates):
    from apps.locations.models import Branch

    names = list(Branch.objects.values_list("name", flat=True))
    assert names == ["Harare branch", "Gweru branch"]  # ordered by `order`


def test_about_page_lists_active_branches(client, branch_with_coordinates, branch_without_coordinates, inactive_branch):
    response = client.get(reverse("core:about"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "Harare branch" in content
    assert "Gweru branch" in content
    assert "Closed branch" not in content


def test_about_page_only_renders_map_container_when_a_pin_exists(client, branch_with_coordinates, branch_without_coordinates):
    response = client.get(reverse("core:about"))
    content = response.content.decode()

    # The Harare branch has coordinates so the map + its JSON data island
    # should render...
    assert 'id="branch-map"' in content
    assert 'id="branch-map-pins"' in content

    # ...and only that branch's coordinates should be in the pin data —
    # the Gweru branch (no lat/lng yet) must not produce a broken pin.
    assert "-17.858" in content


def test_about_page_omits_map_container_when_no_branch_has_coordinates(client, branch_without_coordinates):
    response = client.get(reverse("core:about"))
    content = response.content.decode()

    # Still lists the branch (with a working directions-by-address link)...
    assert "Gweru branch" in content
    # ...but there's nothing to pin, so no empty/broken map should render.
    assert 'id="branch-map"' not in content


def test_about_page_directions_links_present(client, branch_with_coordinates):
    response = client.get(reverse("core:about"))
    assert b"maps/dir/?api=1&amp;destination=-17.858" in response.content
