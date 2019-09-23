import os


def google_apps(request):
    context = {}
    var = 'GOOGLE_APPS_ACCOUNT'

    if var in os.environ:
        context[var.lower()] = os.environ[var]

    return context
