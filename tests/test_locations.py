import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

pytestmark = pytest.mark.django_db

# A valid 1x1 transparent PNG — small enough to inline, real enough that
# Pillow (which ImageField validation relies on) accepts it.
_ONE_PIXEL_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


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

    # Scoped to the rows these fixtures created rather than the whole
    # table: migration 0002 seeds its own "Harare branch" / "Gweru branch"
    # rows into every test database (pytest-django applies all migrations
    # when building it), so `Branch.objects.all()` legitimately contains
    # more than just what this test set up.
    names = list(
        Branch.objects.filter(
            pk__in=[branch_without_coordinates.pk, branch_with_coordinates.pk]
        ).values_list("name", flat=True)
    )
    assert names == ["Harare branch", "Gweru branch"]  # ordered by `order`


def test_about_page_lists_active_branches(client, branch_with_coordinates, branch_without_coordinates, inactive_branch):
    response = client.get(reverse("core:about"))
    content = response.content.decode()

    assert response.status_code == 200
    assert "Harare branch" in content
    assert "Gweru branch" in content
    assert "Closed branch" not in content


def test_about_page_renders_map_image_when_uploaded(client, branch_without_coordinates):
    branch_without_coordinates.map_image = SimpleUploadedFile(
        "gweru.png", _ONE_PIXEL_PNG, content_type="image/png"
    )
    branch_without_coordinates.save()

    response = client.get(reverse("core:about"))
    content = response.content.decode()

    assert 'class="branch-map-image"' in content
    assert branch_without_coordinates.map_image.url in content


def test_about_page_omits_image_tag_when_no_map_image(client, branch_without_coordinates):
    response = client.get(reverse("core:about"))
    content = response.content.decode()

    # Still lists the branch with a working directions button...
    assert "Gweru branch" in content
    # ...but no <img> — nothing was uploaded for it yet.
    assert 'class="branch-map-image"' not in content


def test_about_page_directions_is_styled_as_a_button(client, branch_with_coordinates):
    response = client.get(reverse("core:about"))
    content = response.content.decode()

    assert 'class="btn"' in content
    assert "Get directions" in content


def test_about_page_directions_links_present(client, branch_with_coordinates):
    response = client.get(reverse("core:about"))
    assert b"maps/dir/?api=1&amp;destination=-17.858" in response.content
