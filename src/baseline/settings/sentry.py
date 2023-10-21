import sys

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .environment import ENVIRONMENT, VERSION
from .utils import get_setting

SENTRY_DSN = get_setting("SENTRY_DSN", default=None, maintenance_default=None)
if SENTRY_DSN:
    print(f"SENTRY_DSN={SENTRY_DSN!r}", file=sys.stderr)

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        release=VERSION,
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        # traces_sampler=my_traces_sampler,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )
else:
    print("WARNING: SENTRY_DSN is not defined", file=sys.stderr)
