import os

from baseline.conf.settings.default import *

try:
    from baseline.local_settings import *
except ImportError:
    pass

# check to see if there is a secret key set
try:
    SECRET_KEY
except:
    warn(('Django 1.5 will not run without a SECRET_KEY.  In your environment:'
          'export DJANGO_SECRET_KEY=<some random string>'))
