"""
WSGI config for blwebproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

SETTINGS_ENV_VAR = "DJANGO_SETTINGS_MODULE"
if SETTINGS_ENV_VAR not in os.environ:
    raise EnvironmentError(f"{SETTINGS_ENV_VAR} is required in environment")

application = get_wsgi_application()
