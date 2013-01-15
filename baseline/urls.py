from django.conf.urls import patterns, include, url
from django.conf import settings
from django.utils.importlib import import_module

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = []
for app in settings.LOCAL_APPS:
    try:
        module = import_module('{0}.urls'.format(app))
        urlpatterns += module.urlpatterns
    except ImportError:
        pass

urlpatterns += patterns('',
    # Examples:
    url(r'^$', 'baseline.views.home', name='home'),
    url(r'^404/$', 'baseline.views.notfound', name='404'),
    url(r'^500/$', 'baseline.views.explode', name='500'),
    url(r'^preview/404/$', 'baseline.views.preview', kwargs={'template': '404.html'}, name='404'),
    url(r'^preview/500/$', 'baseline.views.preview', kwargs={'template': '500.html'}, name='500'),
    # url(r'^baseline/', include('baseline.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    url(r'^login/?$', 'django.contrib.auth.views.login', {'template_name': 'baseline/login.html'}, name='login'),
    url(r'^logout/?$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'', include('social_auth.urls')),
)
