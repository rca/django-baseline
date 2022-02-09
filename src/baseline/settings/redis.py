"""
Settings module to configure a basic Redis cache
"""
import os

REDIS_CACHE_URL = os.environ["REDIS_CACHE_URL"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_CACHE_URL,
    }
}
