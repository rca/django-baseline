import os

from baseline.util import warn

from conf.settings.default import *

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

# anything in localsettings overrides the automatically included stuff above
try:
    from localsettings import *
except ImportError:
    pass

# check to see if there is a secret key set either in secretkey.py or environment
if not SECRET_KEY:
    warn('Please create a secret key by running: "manage.py secretkey"')
