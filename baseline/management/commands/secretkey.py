import os
import sys
import string

from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

import baseline

CHARS = string.ascii_letters + string.digits + string.punctuation
SECRET_KEY_PATH = os.path.join(os.path.dirname(baseline.__file__), 'secretkey.py')

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
        if os.path.exists(SECRET_KEY_PATH) and not options['force']:
            print 'Secret key file already exists; use -f to regenerate'
            sys.exit(0)

        random_string = get_random_string(50, CHARS)

        with open(SECRET_KEY_PATH, 'wb') as f:
            f.write('SECRET_KEY = "{0}"\n'.format(random_string))
