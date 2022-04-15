import functools

from django.core.cache import cache


def cached(name: str = None):
    """
    Cache decorator

    Args:
        name: the name to use, otherwise the function name is used
    """

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            cache_key = self.get_cache_key(name or fn.__name__, *args, **kwargs)
            result = cache.get(cache_key)

            if result:
                return result

            result = fn(self, *args, **kwargs)
            cache.set(cache_key, result, timeout=86400 * 7)

            return result

        return wrapper

    return decorator
