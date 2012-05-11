#!/usr/bin/env bash
set +e

# make sure we're in the project directory
SCRIPT_DIR=$(dirname $0)
cd "${SCRIPT_DIR}"

# move origin over to baseline
git remote -v | grep -q '^baseline' || git remote rename origin baseline;

if [ ! -e venv ]; then
    virtualenv venv --distribute
    venv/bin/pip install -r requirements.txt
fi;

# create the virtual environment and install requirements
secret_key=baseline/secretkey.py
if [ ! -e ${secret_key} ]; then
    venv/bin/python manage.py secretkey;

    git add ${secret_key}
    git commit -m"Added ${secret_key}" ${secret_key}
fi;

# create localsettings module
if [ ! -e baseline/localsettings.py ]; then
    echo 'from conf.settings.development import *' >> baseline/localsettings.py
fi;

# sync the local database
python manage.py syncdb
python manage.py migrate
