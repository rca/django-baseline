#!/usr/bin/env bash
set -e

SCRIPT_DIR=$(dirname $0)
[ "${SCRIPT_DIR}" == "." ] && SCRIPT_DIR=$(pwd)

# make sure we're in the project directory
cd "${SCRIPT_DIR}/.."

PROJECT="baseline"

function find_pyc {
    find ${SCRIPT_DIR} -path ${SCRIPT_DIR}/venv -prune -o -type f -name '*.pyc' -print
}

echo "Baseline Bootstrap v1.0"
echo "-----------------------"
echo

# move origin over to baseline
git remote -v | grep -q '^baseline' || git remote rename origin baseline || /bin/true

if [ "$1" == "-h" -o "$1" == "help" -o "$1" == "-?" ]; then
	echo "When run without any arguments, this script sets up the project"
	echo "for running using a virtualenv in the current working directory."
	echo
	echo "The NOINPUT environment variable can be set to '1' (anything not "
	echo "empty, really) in order to run without prompting.  Note: this can "
	echo "be dangerous when combined with clean / superclean"
	echo
	echo "Usage: $0 [-h|--noinput|clean]"
	echo
	echo "  help         display this help"
	echo "  clean        remove all .pyc files"
	echo
	exit
fi

if [ "$1" == "clean" ]; then
    echo "Files to delete:"
    find_pyc | sed 's/^/    /'

    if [ -z ${NOINPUT} ]; then
        echo
        echo -n "Are you sure? [y|N]: "

        read input
    else
        input='y'
    fi

	if [ "$input" == "y" -o "$input" == "Y" ]; then
		echo -n "deleting."
        find_pyc | xargs rm -f
		echo ".done"
	else
		echo "Aborting."
	fi
	exit
fi

if [ ! -z ${NOINPUT} ]; then
    manage_args="--noinput"
else
    manage_args=""
fi;

# sync the local database
cd src
python manage.py syncdb $manage_args
python manage.py migrate $manage_args
