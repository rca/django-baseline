import typing

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

if typing.TYPE_CHECKING:
    from django.http import HttpRequest


class CacheViewSet(viewsets.ViewSet):
    """
    Viewset that exposes cache management operations
    """

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAdminUser],
    )
    def clear(self, request: "HttpRequest", **kwargs) -> "Response":
        """
        Flushes the entire cache

        Note: this is a very heavy-handed thing to do and should only be done in extreme circumstances.
        """
        from django.core.cache import caches

        cache = caches["default"]

        response = cache.clear()

        response_data = {
            "response": str(response),
        }

        return Response(response_data)
