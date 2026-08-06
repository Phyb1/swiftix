# Swiftix Auto Hybrid & Programming Solutions

Django site for a hybrid vehicle service provider: genuine spare parts
catalog + cart, quote-only services, and a promotions/poster gallery —
plus custom error pages and defensive input handling throughout.

## Structure

```
config/settings/     base.py, dev.py, prod.py (python-decouple driven)
apps/catalog/          Category, Product (price nullable = POA)
apps/services/           Service (quote-only, no cart)
apps/posters/             Poster (image + caption + date, admin-managed gallery)
apps/cart/                 session cart + WhatsApp order link builder
apps/core/                  home/about, business-info context processor
apps/core/whatsapp.py      shared wa.me link builder — returns None (not a
                            broken link) if WHATSAPP_ORDER_NUMBER is unset
templates/404.html         custom 404 — extends base.html (context available)
templates/500.html         custom 500 — deliberately standalone, no
                            template inheritance or {{ variables }}, since
                            Django renders this with NO context at all
static_src/, tests/
passenger_wsgi.py         cPanel/Passenger entrypoint
```

## Business info

- Phone / WhatsApp: +263 781 332 627 (alt Gweru line: +263 782 652 594,
  not currently wired in — ask the client which number should take
  WhatsApp orders if that should change)
- Email: swiftixauto@gmail.com
- Harare (primary): No. 1 Tourle Rd, New Ardbennie, Southerton, Harare
- Gweru branch: No. 6052, 58 Street, Shamrock, Gweru (About/footer only,
  per the client's preference not to show both branches on every page)
- Facebook: facebook.com/SwiftixAuto — **unconfirmed URL**, built from the
  page name shown in their profile screenshot rather than a copied link.
  Verify before launch.
- Instagram: @swiftixauto

## Error handling

- **404**: branded, extends `base.html`, offers a WhatsApp fallback link.
- **500**: intentionally standalone HTML with inline CSS — Django renders
  `500.html` with zero context (no request, no context processors), by
  design, since the error might be caused by something in that chain
  being broken. Business phone/WhatsApp number are hardcoded here as a
  result — **if the business's WhatsApp number ever changes, this file
  needs a manual update too**, since it can't read from settings/.env
  like the rest of the site does.
- **Cart quantity input** is parsed defensively (`apps/cart/views.py:
  _parse_quantity`) — non-numeric, missing, negative, or absurdly large
  values fall back to a safe default instead of 500ing the page.
- **`next` redirect parameter** (used after adding to cart) is validated
  against `url_has_allowed_host_and_scheme` before being followed, to
  prevent an open-redirect if that field is ever tampered with.
- **WhatsApp links** degrade gracefully: if `WHATSAPP_ORDER_NUMBER` is
  ever blank/misconfigured, `whatsapp_link()` returns `None` rather than
  a broken `wa.me/` URL, and every template that uses it falls back to
  showing the phone/email instead of a dead button.
- **Posters without an image** render the placeholder instead of raising
  — same pattern as Product/Service `display_image_url`.

## Local setup (Termux/mobile friendly)

```bash
pip install -r requirements.txt --break-system-packages
cp .env.example .env          # edit SECRET_KEY at minimum
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Adding parts, services & posters

All managed through `/admin/` (Swiftix-branded — orange/navy theme):

- **Categories** first (Computer Boxes, Gearboxes, Dual Clutch, Service
  Kits, Suspension Kits, Bearings, Plugs & Consumables — or whatever set
  the client actually wants), then **Products**. Leave price blank only
  if a part genuinely needs POA — the client asked for fixed pricing as
  the default here.
- **Services**: Vehicle Diagnosis, Hybrid Battery Service, Engine
  Service, Key Programming, ECU Programming — quote-only, no price shown.
- **Posters**: upload the same images they're already posting to
  WhatsApp status/Facebook — caption + date, shows newest-first on
  `/promotions/` and the 4 most recent also surface on the homepage.

## Running tests

```bash
pytest
```

Covers everything from the OnSpot build (slugs, POA pricing, cart
lifecycle, category/service filtering) plus this project's additions:
poster gallery ordering and active-only filtering, the placeholder
fallback for posters with no image attached, custom 404/500 page
rendering, and the cart's defensive input handling (bad quantity values,
open-redirect attempts via `next`).

## Deploying to cPanel/Passenger

Same pattern as OnSpot/Shato/Samwa/Mimie's — see that project's README
for the full walkthrough if this is deployed under a domain root. If it
ends up on a **sub-path** (e.g. `yourdomain.com/swiftix/`) instead, the
OnSpot project's debugging history is essential reading first: that
exact setup needed `STATIC_URL`/`MEDIA_URL` set explicitly in `.env`
*and* an explicit Django URL route for static/media (see this project's
`config/urls.py` — it's already carried over) because Passenger strips
the sub-path before Django ever sees the request, which breaks
WhiteNoise's normal static-file matching. Don't re-diagnose that from
scratch — the fix is already baked into this codebase, just uncomment
the `STATIC_URL`/`MEDIA_URL` lines in `.env.example` if needed.

## Notes / things to confirm with the client before launch

- **Facebook URL is a guess** (`facebook.com/SwiftixAuto`) — the
  screenshot showed the page name but not the actual profile URL. Get
  the real link before this ships.
- Second WhatsApp/phone number (+263 782 652 594) shown on their poster
  isn't wired in anywhere — confirm whether that should be the Gweru
  branch's contact point somewhere on the site.
- Seed real product/service/poster content with actual photos before
  sharing a demo link — placeholders are fine for review, not launch.
