import os
import sys

from optparse import make_option

from django.core.management.base import BaseCommand

import baseline

from baseline.conf.settings.default import get_project_root
from baseline.settings import warn

LOCAL_URLS_PATH = os.path.join(os.path.dirname(baseline.__file__), 'localurls.py')

LOCALURLS_TEMPLATE = """from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
    url(r'', include('{0}.urls')),
)
"""

APP_URLS_TEMPLATE = """from django.conf.urls import patterns, include, url
urlpatterns = patterns('{app}.views',
    url(r'^$', 'home', name="{app}_home"),
)
"""

HELLO_VIEW = """def home(request):
    from django.shortcuts import render_to_response
    return render_to_response('baseline/app_home.html', {})
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
            app = args[0].replace('/','')
        except IndexError:
            self.print_help('manage.py', 'localurls')
            warn('App not given', color='red', name='Error', print_traceback=False, prefix='\n')
            sys.exit(1)

        app_root = os.path.join(get_project_root(), app)
        if not os.path.exists(app_root):

            warn('App does not exist; create app using django-admin.py startapp {0}'.format(app),
                 color='red', name='Error', print_traceback=False)
            sys.exit(1)

        with open(LOCAL_URLS_PATH, 'wb') as f:
            f.write(LOCALURLS_TEMPLATE.format(app))

        with open(os.path.join(app_root, 'urls.py'), 'wb') as f:
            f.write(APP_URLS_TEMPLATE.format(app=app))

        with open(os.path.join(app_root, 'views.py'), 'ab') as f:
            f.write(HELLO_VIEW)
