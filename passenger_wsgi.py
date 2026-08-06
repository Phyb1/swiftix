import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

# Add virtualenv site-packages so Passenger can find Django
sys.path.insert(0, os.path.join(
    os.path.dirname(__file__),
    'virtualenv/onspot/public_html/3.11/lib/python3.11/site-packages'
))

# Set settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
