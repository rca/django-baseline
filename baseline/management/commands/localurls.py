import os
import sys

from optparse import make_option

from django.core.management.base import BaseCommand

import baseline

LOCAL_URLS_PATH = os.path.join(os.path.dirname(baseline.__file__), 'localurls.py')

TEMPLATE = """from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'', include('{0}.urls')),
)
"""

class Command(BaseCommand):
    args = 'app'
    help = "Generate localurls module that points to the given app's urls"

    can_import_settings = False

    def __init__(self):
        super(Command, self).__init__()

        self.option_list += (
            make_option('-f', '--force', action='store_true', help='Regenerate secret key'),
            )

    def handle(self, *args, **options):
        if os.path.exists(LOCAL_URLS_PATH) and not options['force']:
            print 'localurls file already exists; use -f to regenerate'
            sys.exit(0)

        try:
            app = args[0]
        except IndexError:
            from baseline.settings import warn

            self.print_help('manage.py', 'localurls')
            warn('App not given', color='red', name='Error', print_traceback=False, prefix='\n')
            sys.exit(1)

        with open(LOCAL_URLS_PATH, 'wb') as f:
            f.write(TEMPLATE.format(app))
