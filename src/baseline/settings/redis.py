"""
Settings module to configure a basic Redis cache
"""
from .utils import get_setting

REDIS_CACHE_URL = get_setting("REDIS_CACHE_URL")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_CACHE_URL,
    }
}
