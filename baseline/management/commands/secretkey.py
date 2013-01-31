import os
import sys
import string

from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

import baseline

from baseline.util import HerokuError, get_heroku_config, set_heroku_config, warn

CHARS = string.ascii_letters + string.digits + string.punctuation.replace('"', '')

LOCALSETTINGS = os.path.join(os.path.dirname(baseline.__file__), 'local_settings.py')

class Command(BaseCommand):
    args = ''
    help = 'Generate a secret key'

    can_import_settings = False

    def __init__(self):
        super(Command, self).__init__()

        self.option_list += (
            make_option('-f', '--force', action='store_true', help='Regenerate secret key'),
        )

    def handle(self, *args, **options):
        try:
            heroku_config = get_heroku_config()
        except HerokuError:
            heroku_config = {}

        # check to see if the secret key is already set
        try:
            from baseline import local_settings

            if hasattr(local_settings, 'SECRET_KEY') and not options['force']:
                print 'Secret key already created; use -f to regenerate'
                sys.exit(0)
        except ImportError, exc:
            print exc
            pass

        random_string = heroku_config.get('DJANGO_SECRET_KEY', None) or \
                get_random_string(50, CHARS)

        with open(LOCALSETTINGS, 'ab') as f:
            f.write('SECRET_KEY = {0!r}\n'.format(random_string))

        try:
            set_heroku_config(DJANGO_SECRET_KEY=random_string)
        except HerokuError, msg:
            message = 'Unable to set heroku config.  Make sure to run:\n  {0}'.format(msg[1])
            warn(message, name='Warning')
