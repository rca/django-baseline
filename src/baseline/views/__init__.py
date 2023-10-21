from rest_framework.viewsets import GenericViewSet

from ..utils import get_package_items

__locals = locals()
for item in get_package_items(__file__, __name__, GenericViewSet):
    __locals[item.__name__] = item
