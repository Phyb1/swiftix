from django.conf import settings


def site_settings(request):
    return {
        "SITE_NAME": settings.SITE_NAME,
        "WHATSAPP_ORDER_NUMBER": settings.WHATSAPP_ORDER_NUMBER,
        "BUSINESS_PHONE_DISPLAY": settings.BUSINESS_PHONE_DISPLAY,
        "BUSINESS_EMAIL": settings.BUSINESS_EMAIL,
        "BUSINESS_ADDRESS": settings.BUSINESS_ADDRESS,
        "GWERU_ADDRESS": settings.GWERU_ADDRESS,
        "FACEBOOK_URL": settings.FACEBOOK_URL,
        "INSTAGRAM_URL": settings.INSTAGRAM_URL,
    }
