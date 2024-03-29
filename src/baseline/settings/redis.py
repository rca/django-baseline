"""
Settings module to configure a basic Redis cache
"""
from .utils import get_setting

REDIS_CACHE_URL = get_setting(
    "REDIS_CACHE_URL",
    maintenance_default="redis://redis:6379/0",
)

REDIS_CACHE_TIMEOUT = int(
    get_setting(
        "REDIS_CACHE_TIMEOUT",
        default=86400 * 365,
    )
)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_CACHE_URL,
        "TIMEOUT": REDIS_CACHE_TIMEOUT,
    }
}
