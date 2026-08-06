from .base import *  # noqa: F401,F403
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = ["127.0.0.1"]
