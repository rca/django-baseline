import os
import sys

from optparse import make_option

from django.core.management.base import BaseCommand

import baseline

from baseline.conf.settings.default import get_project_root
from baseline.settings import warn

LOCAL_APPS_PATH = os.path.join(os.path.dirname(baseline.__file__), 'localapps.py')
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

LOCALAPPS_TEMPLATE = """# auto-generated file by manage.py localapp
LOCAL_APPS = {LOCAL_APPS}
"""

HELLO_VIEW = """def home(request):
    from django.shortcuts import render_to_response
    return render_to_response('baseline/app_home.html', {})
"""

class Command(BaseCommand):
    args = 'app'
    help = "Add local application to project.  First app will have its URLs automatically included."

    can_import_settings = False

    def __init__(self):
        super(Command, self).__init__()

        self.option_list += (
            make_option('-f', '--force', action='store_true', help='Regenerate secret key'),
            )

    def handle(self, *args, **options):
        LOCAL_APPS = ()

        try:
            # tab completion may have added a slash, so remove it.
            app = args[0].replace('/','')
        except IndexError:
            self.print_help('manage.py', 'localapp')
            warn('App not given', color='red', name='Error', print_traceback=False, prefix='\n')
            sys.exit(1)

        app_root = os.path.join(get_project_root(), app)
        if os.path.exists(LOCAL_APPS_PATH):
            with open(LOCAL_APPS_PATH, 'rb') as f:
                t_content = f.read()

                exec t_content # redefines LOCAL_APPS to contain existing apps.
        elif os.path.exists(app_root): # project's first app, tie in its urls.
            with open(LOCAL_URLS_PATH, 'wb') as f:
                f.write(LOCALURLS_TEMPLATE.format(app))

            with open(os.path.join(app_root, 'urls.py'), 'wb') as f:
                f.write(APP_URLS_TEMPLATE.format(app=app))

            # create a stub view; use append to not accidentally blow away
            # user-generated views.
            with open(os.path.join(app_root, 'views.py'), 'ab') as f:
                f.write(HELLO_VIEW)

        # add this app to LOCAL_APPS
        LOCAL_APPS += (app,)

        # ensure no dupes and maintain order in which apps were added.
        t_apps = []
        for t_app in LOCAL_APPS:
            if t_app not in t_apps:
                t_apps.append(t_app)

        # create the localapps.py file
        with open(LOCAL_APPS_PATH, 'wb') as f:
            f.write(LOCALAPPS_TEMPLATE.format(LOCAL_APPS=tuple(t_apps)))
