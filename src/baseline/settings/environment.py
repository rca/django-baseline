import sys

from .utils import get_setting

ENVIRONMENT = get_setting("CF_ENV", default="unknown")
VERSION = get_setting("VERSION", required=False)

print(f"ENVIRONMENT={ENVIRONMENT}, VERSION={VERSION}", file=sys.stderr)
