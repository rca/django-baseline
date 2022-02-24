from rest_framework import routers


class PrefixBasenameSimpleRouter(routers.SimpleRouter):
    def register(self, prefix, viewset, basename=None):
        basename = basename or prefix

        super().register(prefix, viewset, basename)
