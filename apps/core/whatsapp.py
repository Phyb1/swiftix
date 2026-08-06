import logging
from urllib.parse import quote

from django.conf import settings

logger = logging.getLogger(__name__)


def whatsapp_link(message: str) -> str | None:
    """Build a wa.me link for the configured business WhatsApp number.

    Returns None (rather than a broken link) if WHATSAPP_ORDER_NUMBER is
    missing or obviously malformed, and logs a warning so it surfaces in
    ops/monitoring rather than failing silently in front of a customer.
    """
    number = getattr(settings, "WHATSAPP_ORDER_NUMBER", "")
    digits_only = "".join(ch for ch in number if ch.isdigit())

    if not digits_only:
        logger.warning("WHATSAPP_ORDER_NUMBER is unset or invalid: %r", number)
        return None

    return f"https://wa.me/{digits_only}?text={quote(message)}"
