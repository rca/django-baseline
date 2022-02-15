"""
Celery settings module
"""
from .utils import get_setting

# Celery settings
CELERY_BROKER_URL = get_setting("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = get_setting("CELERY_RESULT_BACKEND")
