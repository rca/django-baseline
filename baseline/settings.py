import sys

from conf.settings.default import *

def warn(message, color='yellow', name='Warning'):
    import sys, traceback
    from django.utils.termcolors import make_style

    red = make_style(fg=color, opts=('bold',))

    traceback.print_exc()
    sys.stderr.write('{0}: {1}\n'.format(red(name), message))

try:
    from secretkey import SECRET_KEY
except ImportError:
    warn('Please create a secret key by running: "manage.py secretkey"')

try:
    from localsettings import *
except ImportError:
    warn('Unable to import localsettings.py')
