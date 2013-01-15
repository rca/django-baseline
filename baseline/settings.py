from django.utils.importlib import import_module
import os

from baseline.util import convert_bool, convert_int, warn

from baseline.conf.settings.default import *

# stub in SECRET_KEY and see if it's set by bringing in environment variables
SECRET_KEY = None

try:
    from local_apps import LOCAL_APPS
    INSTALLED_APPS += LOCAL_APPS
except ImportError:
    LOCAL_APPS = ()
    pass

# get settings from all local apps
app_settings = {}
for app in LOCAL_APPS:
    try:
        module = import_module('{0}.settings'.format(app))
        for item in dir(module):
            app_settings[item] = getattr(module, item)
    except ImportError:
        pass
locals().update(app_settings)

# Parse database configuration from $DATABASE_URL
import dj_database_url
dj_db_config = dj_database_url.config()
if dj_db_config:
    DATABASES['default'] =  dj_database_url.config()

# create settings variables for any environment variable prefixed 'DJANGO_.*'
# this removes the DJANGO_ prefix
prefix = 'DJANGO_'
for key in os.environ:
    _locals = locals()

    if key.startswith(prefix):
        value = os.environ[key]

        # int first
        value = convert_int(value)
        # truthy/falsy values second
        value = convert_bool(value)

        _locals[key[len(prefix):]] = value

# check to see if there is a secret key set either in secretkey.py or environment
if not SECRET_KEY:
    warn('Please create a secret key by running: "manage.py secretkey"')
