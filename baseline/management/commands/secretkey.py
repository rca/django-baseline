import os
import re
import string

from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from baseline.util import get_project_root

CHARS = string.ascii_letters + string.digits + string.punctuation.replace("'", '')
ENV_RE = re.compile(r"export (?P<key>.*)=[\"']?(?P<value>.*)[\"']?")
ENV_FILE = '.env'
SECRET_KEY_NAME = 'DJANGO_SECRET_KEY'


class Command(BaseCommand):
    args = ''
    help = 'Generate a secret key'

    can_import_settings = False

    def __init__(self):
        super(Command, self).__init__()

        self.option_list += (
            make_option('-f', '--force', action='store_true', help='Regenerate secret key'),
        )

    @property
    def env_path(self):
        project_root = get_project_root()        
        return os.path.join(project_root, ENV_FILE)

    def read_env_file(self):
        env = {}

        if not os.path.exists(self.env_path):
            return env

        with open(self.env_path, 'rb') as env_fh:
            while True:
                line = env_fh.readline()
                if line == '':
                    break

                line = line.strip()
                matches = ENV_RE.match(line)
                if matches:
                    env[matches.group('key')] = matches.group('value')

        return env

    def handle(self, *args, **options):
        env = self.read_env_file()

        if SECRET_KEY_NAME not in env:
            random_string = get_random_string(50, CHARS)
            line = "export {0}='{1}'\n".format(SECRET_KEY_NAME, random_string)

            with open(self.env_path, 'ab') as env_fh:
                env_fh.write(line)

        print "You're all set, make sure you run: 'source {}'".format(self.env_path)
