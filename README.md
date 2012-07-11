Django Baseline
===============

Django Baseline is a ready-made Django project that helps you deploy to Heroku and get working on your application.

Getting Started
---------------

Clone this repo with your desired project name:

```
git clone git://github.com/rca/django-baseline.git myproject
cd myproject
```

Run the bootstrap script.  This script will rename the baseline remote repo to
baseline so that origin is left open for your project.  It will also create a
virtual environment in the ```venv``` directory, create a secret key file as a
seed for Django's crypto functions, create a localsettings module, which
enables debug, and sync databases for local development.

```
./bootstrap.sh
```

Deploying to Heroku
-------------------

Initialize heroku in the project directory and push to Heroku:

```
heroku create --stack cedar
git push heroku master
```

Sync the database:

```
heroku run python manage.py syncdb
heroku run python manage.py migrate
```

And view your application:

```
heroku open
```

Developing your app
-------------------

First, activate your virtualenv:

```
. venv/bin/activate
```

Create your application:

```
django-admin.py startapp myapp
git add myapp
git commit -m'Added django app, "myapp"'
```

Add your app, tie in its urls module, and commit:

```
python manage.py localapp myapp
git add -A
git commit -m'Added baseline-generated files'
```

Run your local server and access your site at http://localhost:8000/

```
python manage.py runserver
```

Application Settings
--------------------

The settings.py file in any apps listed in baseline/localapps.py will be added
to the Django settings.  Any sensitive data, such as passwords, should not be
kept in settings files that end up in the repository but rather in environment
variables.  Setting up environment variables in heroku can be set using
```heroku config```.  More information at
https://devcenter.heroku.com/articles/config-vars

Any environment variable that starts with ```DJANGO_``` will be automatically
added to settings with the prefix removed.  For example, DJANGO_FOO will end up
being FOO in Django's settings.

For development, you can add these to your environment before running django,
or add the variables to localsettings.py.

Happy Hacking
-------------

You're on your way.  If this is your first time diving into Django take a look
at its excellent documentation at https://docs.djangoproject.com/en/1.4/
