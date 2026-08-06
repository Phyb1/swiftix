from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.catalog.models import Product
from apps.core.whatsapp import whatsapp_link

from .cart import Cart

MAX_QUANTITY = 999


def _parse_quantity(raw, default=1):
    """Safely parse a quantity from POST data. Never raises — falls back
    to `default` on missing/non-numeric input, and clamps to a sane range
    so a typo or tampered form can't 500 the page or queue up an absurd
    order quantity."""
    try:
        quantity = int(raw)
    except (TypeError, ValueError):
        return default
    return max(1, min(quantity, MAX_QUANTITY))


def _safe_redirect_target(request, fallback_url_name="cart:cart_detail"):
    """Only follow a POSTed `next` value if it's a safe same-site path.
    Prevents an open-redirect if `next` is ever tampered with."""
    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return next_url
    return reverse(fallback_url_name)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, in_stock=True)
    target = _safe_redirect_target(request)

    if product.is_poa:
        messages.info(
            request,
            f"{product.name} is priced on request — please enquire on WhatsApp instead.",
        )
        return redirect(target)

    quantity = _parse_quantity(request.POST.get("quantity"), default=1)
    cart.add(product=product, quantity=quantity)
    messages.success(request, f"Added {product.name} to your bag.")
    return redirect(target)


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = _parse_quantity(request.POST.get("quantity"), default=1)
    cart.update_quantity(product, quantity)
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"Removed {product.name} from your bag.")
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    whatsapp_link = build_whatsapp_order_link(cart) if len(cart) else None
    return render(
        request,
        "cart/cart_detail.html",
        {"cart": cart, "whatsapp_link": whatsapp_link},
    )


def build_whatsapp_order_link(cart):
    lines = [f"Hi {settings.SITE_NAME}, I'd like to order:"]
    for item in cart:
        lines.append(
            f"- {item['product'].name} x{item['quantity']} "
            f"(${item['subtotal']:.2f})"
        )
    lines.append(f"Total: ${cart.get_total_price():.2f}")
    return whatsapp_link("\n".join(lines))
