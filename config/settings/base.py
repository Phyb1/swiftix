"""
Base settings for Swiftix Auto Hybrid & Programming Solutions.
Environment-specific settings live in dev.py / prod.py.
"""
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-me-in-env")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local apps
    "apps.catalog",
    "apps.services",
    "apps.posters",
    "apps.cart",
    "apps.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Harare"
USE_I18N = True
USE_TZ = True

STATIC_URL = config("STATIC_URL", default="/static/")
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static_src"]

# Django 4.2+ replaces STATICFILES_STORAGE/DEFAULT_FILE_STORAGE with STORAGES.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = config("MEDIA_URL", default="/media/")
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Swiftix Auto Hybrid & Programming Solutions business settings ---
# WhatsApp number orders/enquiries are sent to, international format, no + or spaces.
# --- Swiftix Auto Hybrid & Programming Solutions business settings ---
# WhatsApp number orders/enquiries are sent to, international format, no + or spaces.
WHATSAPP_ORDER_NUMBER = config("WHATSAPP_ORDER_NUMBER", default="263781332627")
SITE_NAME = config("SITE_NAME", default="Swiftix Auto Hybrid & Programming Solutions")
BUSINESS_PHONE_DISPLAY = config("BUSINESS_PHONE_DISPLAY", default="+263 781 332 627")
BUSINESS_EMAIL = config("BUSINESS_EMAIL", default="swiftixauto@gmail.com")
BUSINESS_ADDRESS = config("BUSINESS_ADDRESS", default="No. 1 Tourle Rd, New Ardbennie, Southerton, Harare, Zimbabwe")
GWERU_ADDRESS = config("GWERU_ADDRESS", default="No. 6052, 58 Street, Shamrock, Gweru, Zimbabwe")
FACEBOOK_URL = config("FACEBOOK_URL", default="https://facebook.com/SwiftixAuto")
INSTAGRAM_URL = config("INSTAGRAM_URL", default="https://instagram.com/swiftixauto")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "WARNING",
    },
}
