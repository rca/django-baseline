from django.utils.importlib import import_module
import os

from baseline.util import warn

from baseline.conf.settings.default import *

try:
    from localapps import LOCAL_APPS
    INSTALLED_APPS += LOCAL_APPS
except ImportError:
    LOCAL_APPS = ()
    pass

# stub in SECRET_KEY and see if it's set by bringing in environment variables
SECRET_KEY = ''

# create settings variables for any environment variable prefixed 'DJANGO_.*'
# this removes the DJANGO_ prefix
for key in os.environ:
    if key.startswith('DJANGO_'):
        setting = '{0} = {1!r}'.format(key[7:], os.environ[key])
        exec setting

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

# anything in localsettings overrides the automatically included stuff above
try:
    from baseline.localsettings import *
except ImportError:
    pass

# check to see if there is a secret key set either in secretkey.py or environment
if not SECRET_KEY:
    warn('Please create a secret key by running: "manage.py secretkey"')

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()
