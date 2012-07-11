#!/usr/bin/env bash
set +e

LOCALSETTINGS=baseline/localsettings.py

PIP=venv/bin/pip
PYTHON=venv/bin/python

# make sure we're in the project directory
SCRIPT_DIR=$(dirname $0)
cd "${SCRIPT_DIR}"

# move origin over to baseline
git remote -v | grep -q '^baseline' || git remote rename origin baseline;

if [ ! -e venv ]; then
    virtualenv venv --distribute
    ${PIP} install -r requirements.txt
fi;

# create localsettings module
if [ ! -e ${LOCALSETTINGS} ]; then
    echo 'from conf.settings.development import *' >> ${LOCALSETTINGS}
fi;

# create the virtual environment and install requirements
got_secret_key=$(grep SECRET_KEY ${LOCALSETTINGS})
if [ "$?" -ne "0" ]; then
    ${PYTHON} manage.py secretkey;
else
    echo "got secret"
fi;

# sync the local database
${PYTHON} manage.py syncdb
${PYTHON} manage.py migrate
