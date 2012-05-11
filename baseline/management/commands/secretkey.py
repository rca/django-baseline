import os
import sys
import string

from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

import baseline

from baseline.util import get_heroku_config, set_heroku_config

CHARS = string.ascii_letters + string.digits + string.punctuation.replace('"', '')

LOCALSETTINGS = os.path.join(os.path.dirname(baseline.__file__), 'localsettings.py')

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
        heroku_config = get_heroku_config()

        if 'DJANGO_SECRET_KEY' in heroku_config and not options['force']:
            print 'Secret key already created; use -f to regenerate'
            sys.exit(0)

        random_string = get_random_string(50, CHARS)

        set_heroku_config(DJANGO_SECRET_KEY=random_string)

        with open(LOCALSETTINGS, 'ab') as f:
            f.write('SECRET_KEY = {0!r}\n'.format(random_string))
