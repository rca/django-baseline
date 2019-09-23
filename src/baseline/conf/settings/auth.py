from django.conf.global_settings import AUTHENTICATION_BACKENDS, TEMPLATE_CONTEXT_PROCESSORS

LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/login-error/'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleBackend',
) + AUTHENTICATION_BACKENDS

TEMPLATE_CONTEXT_PROCESSORS += (
    'social_auth.context_processors.social_auth_by_type_backends',
)

SOCIAL_AUTH_ENABLED_BACKENDS = (
    'google',
)
