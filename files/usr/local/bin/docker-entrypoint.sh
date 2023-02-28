#!/bin/bash
set -e
set -x

# automatically run migrations
python manage.py migrate

run-celery &

exec "$@"
