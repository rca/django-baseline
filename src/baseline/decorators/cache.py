import functools

from django.core.cache import cache


def cached(name: str = None, timeout=None):
    """
    Cache decorator

    Args:
        name: the name to use, otherwise the function name is used
        timeout: the amount of time (in seconds) to persist the data in
        the cache
    """

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            cache_key = self.get_cache_key(name or fn.__name__, *args, **kwargs)
            result = cache.get(cache_key)

            if result:
                return result

            result = fn(self, *args, **kwargs)
            timeout_arg = {}
            if timeout:
                timeout_arg["timeout"] = timeout
            cache.set(cache_key, result, **timeout_arg)

            return result

        return wrapper

    return decorator
