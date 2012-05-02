from conf.settings.default import *

try:
    from localsettings import *
except ImportError:
    import sys, traceback
    from django.utils.termcolors import make_style

    yellow = make_style(fg='yellow', opts=('bold',))

    traceback.print_exc()
    sys.stderr.write('{0}: Unable to import localsettings.py\n'.format(yellow('Warning')))
