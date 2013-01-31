from django.utils.importlib import import_module
import os

from baseline.util import convert_bool, convert_int, convert_sequence, warn

from baseline.conf.settings.default import *

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
        if key == 'DJANGO_SETTINGS_MODULE':
            continue

        value = os.environ[key]

        # int first
        value = convert_int(value)
        # truthy/falsy values second
        value = convert_bool(value)
        # value = convert sequences like lists and tuples
        value = convert_sequence(value)

        _locals[key[len(prefix):]] = value

# check to see if there is a secret key set
try:
    SECRET_KEY
except:
    warn(('Django 1.5 will not run without a SECRET_KEY.  In your environment:'
          'export DJANGO_SECRET_KEY=<some random string>'))
