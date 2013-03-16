import os

from baseline.util import convert_bool, convert_int, convert_sequence, warn


# Parse database configuration from $DATABASE_URL
import dj_database_url
dj_db_config = dj_database_url.config()
if dj_db_config:
    DATABASES['default'] =  dj_database_url.config()

# create settings variables for any environment variable prefixed 'DJANGO_.*'
# this removes the DJANGO_ prefix
prefix = 'DJANGO_'
for key in os.environ:
    _locals = locals()

    if key.startswith(prefix):
        if key == 'DJANGO_SETTINGS_MODULE':
            continue

        new_key = key[len(prefix):]
        value = os.environ[key]

        # int first
        value = convert_int(value)
        # truthy/falsy values second
        value = convert_bool(value)
        # value = convert sequences like lists and tuples
        value = convert_sequence(value)

        _locals[new_key] = value
