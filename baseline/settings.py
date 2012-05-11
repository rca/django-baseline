import sys

from conf.settings.default import *

def warn(message, color='yellow', name='Warning', prefix='', print_traceback=True):
    import sys
    from django.utils.termcolors import make_style

    red = make_style(fg=color, opts=('bold',))

    if print_traceback:
        import traceback
        traceback.print_exc()

    sys.stderr.write('{0}{1}: {2}\n'.format(prefix, red(name), message))

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
