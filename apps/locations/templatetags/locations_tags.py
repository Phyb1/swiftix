from django import template

from ..models import Branch

register = template.Library()


@register.inclusion_tag("locations/branch_map.html")
def branch_map_widget():
    """Renders each active branch as a card: an optional admin-uploaded
    location image, address, and a directions button.

    Self-contained: queries the DB itself, so any template can just do
        {% load locations_tags %}
        {% branch_map_widget %}
    with no view/context changes required. Copy this whole app into
    another client project to reuse it there.
    """
    return {"branches": Branch.objects.filter(is_active=True)}
