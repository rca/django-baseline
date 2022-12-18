"""
Celery settings module

The most salient point of the Django docs is on the following page:

https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#using-celery-with-django

and it describes how to go about converting the new-style lowercased settings into `CELERY_` prefixed
variables:

> The uppercase name-space means that all Celery configuration options must be
> specified in uppercase instead of lowercase, and start with CELERY_, so for
> example the task_always_eager setting becomes CELERY_TASK_ALWAYS_EAGER, and
> the broker_url setting becomes CELERY_BROKER_URL. This also applies to the
> workers settings, for instance, the worker_concurrency setting becomes
> CELERY_WORKER_CONCURRENCY.
"""
from conversion import convert_bool

from .utils import get_setting, is_maintenance

# by default use Redis as a pubsub broker
CELERY_BROKER_URL = get_setting(
    "CELERY_BROKER_URL", maintenance_default="redis://redis:6379/1"
)

# also use Redis as the result backend
CELERY_RESULT_BACKEND = get_setting(
    "CELERY_RESULT_BACKEND", maintenance_default="redis://redis:6379/2"
)

# setting late acks is optimizing for a volatile container-based deployment
# where workers can be killed without warning.  this will allow tasks that
# were actively being worked on to still be on the queue and picked up by
# another worker ... eventually; once the worker processing the job is deemed
# gone.
CELERY_TASK_ACKS_LATE = convert_bool(
    get_setting("CELERY_TASK_ACKS_LATE", default="True")
)

# this is great for testing where tasks will be run on the same process rather
# than being queued up.
_is_maintenance = str(is_maintenance())
CELERY_TASK_ALWAYS_EAGER = convert_bool(
    get_setting("CELERY_TASK_ALWAYS_EAGER", default=_is_maintenance)
)
print(
    f"CELERY_TASK_ALWAYS_EAGER={CELERY_TASK_ALWAYS_EAGER}, _is_maintenance={_is_maintenance}"
)

# CELERY_TASK_EAGER_PROPAGATES = convert_bool(
#     get_setting("CELERY_TASK_EAGER_PROPAGATES", default="False")
# )

# in conjunction with late acks, this will attempt to re-queue tasks that
# were pulled down but were not processed.
CELERY_TASK_REJECT_ON_WORKER_LOST = convert_bool(
    get_setting("CELERY_TASK_REJECT_ON_WORKER_LOST", default="true")
)

# attempt to prevent memory leaks in a worker by limiting the number of tasks
# it processes before being terminated and replaced with another process
CELERY_WORKER_MAX_TASKS_PER_CHILD = int(
    get_setting("CELERY_WORKER_MAX_TASKS_PER_CHILD", default="50")
)

# allow the worker to only prefetch a single task per worker thread.  this
# prevents short-running tasks from getting stuck on a worker that's busy
# with long-running tasks; think about getting stuck in the slow lane at
# a grocery store when all the other lanes are zipping along.  NOTE: this
# is at the expense of having latency receiving tasks from the broker, and is
# best suited for systems where it's much more expensive to process a task than
# it is to fetch it from the broker.
CELERY_WORKER_PREFETCH_MULTIPLIER = int(
    get_setting("CELERY_WORKER_PREFETCH_MULTIPLIER", default="1")
)
