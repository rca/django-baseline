import os

from baseline.util import warn

from conf.settings.default import *

try:
    from localapps import LOCAL_APPS
    INSTALLED_APPS += LOCAL_APPS
except ImportError:
    LOCAL_APPS = ()
    pass

try:
    from secretkey import SECRET_KEY
except ImportError:
    SECRET_KEY = ''
    warn('Please create a secret key by running: "manage.py secretkey"')

try:
    from localsettings import *
except ImportError:
    pass

# create settings variables for any environment variable prefixed 'DJANGO_.*'
for key in os.environ:
    if key.startswith('DJANGO_'):
        setting = '{0} = {1!r}'.format(key[7:], os.environ[key])
        exec setting
