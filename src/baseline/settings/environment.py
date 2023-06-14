from .utils import get_setting

ENVIRONMENT = get_setting("ENVIRONMENT", default="unknown")
VERSION = get_setting("VERSION", required=False)
