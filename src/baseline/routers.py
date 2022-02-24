from django.conf import settings
from rest_framework import routers


class PrefixBasenameSimpleRouter(routers.SimpleRouter):
    def __init__(self, trailing_slash=None):
        if trailing_slash is None:
            trailing_slash = settings.TRAILING_SLASH

        super().__init__(trailing_slash)

    def register(self, prefix, viewset, basename=None):
        basename = basename or prefix

        super().register(prefix, viewset, basename)
