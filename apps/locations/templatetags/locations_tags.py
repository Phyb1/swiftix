from django import template

from ..models import Branch

register = template.Library()


@register.inclusion_tag("locations/branch_map.html")
def branch_map_widget():
    """Renders an interactive map with a pin per active Branch that has
    coordinates, plus a text list (with directions links) for all active
    branches — including any that don't have coordinates yet.

    Self-contained: queries the DB itself, so any template can just do
        {% load locations_tags %}
        {% branch_map_widget %}
    with no view/context changes required. Copy this whole app into
    another client project to reuse it there.
    """
    branches = Branch.objects.filter(is_active=True)
    pins = [
        {
            "name": branch.name,
            "address": branch.address,
            "lat": float(branch.latitude),
            "lng": float(branch.longitude),
            "directions_url": branch.get_directions_url(),
        }
        for branch in branches
        if branch.has_coordinates
    ]
    return {"branches": branches, "pins": pins}
