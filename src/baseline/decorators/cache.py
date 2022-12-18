import functools

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.http import condition
from django.views.decorators.vary import vary_on_headers


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


def combined_cache_control(
    max_age, etag_func, last_modified_func, cache_control_kwargs=None, vary_headers=None
):
    _max_age = max_age
    _cache_control_kwargs = cache_control_kwargs or dict(must_revalidate=True)
    _vary_headers = vary_headers or ("Authorization",)
    _etag_func = etag_func
    _last_modified_func = last_modified_func

    """
    A single decorator to apply all the headers needed for high-performance page caching
    """

    def decorator(fn):
        return method_decorator(vary_on_headers(*_vary_headers))(
            method_decorator(cache_control(max_age=_max_age, **_cache_control_kwargs))(
                method_decorator(
                    condition(
                        etag_func=_etag_func,
                        last_modified_func=_last_modified_func,
                    )
                )(fn)
            )
        )

    return decorator
