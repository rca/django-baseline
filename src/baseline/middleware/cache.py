from django.middleware.cache import FetchFromCacheMiddleware

BUST_MAGIC_CACHE_CONTROL = "x-django-bust-cache"


class BustableFetchFromCacheMiddleware(FetchFromCacheMiddleware):
    """
    The FetchFromCacheMiddleware with an extra bit to be able to bypass cache
    """

    def process_request(self, request):
        # the FetchFromCacheMiddleware alters the request object to notify
        # the UpdateCacheMiddleware on what should be done.  let it do all
        # that stuff so that the cache saving behavior does not change
        response = super().process_request(request)

        # check to see if the cache should be busted.  when this returns
        # None, the view is called.
        cache_control = request.META.get("HTTP_CACHE_CONTROL", "")
        if BUST_MAGIC_CACHE_CONTROL in cache_control:
            return None

        return response
