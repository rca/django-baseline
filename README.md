Django Baseline
===============

Django Baseline is a ready-made Django project that eliminates the boilerplate.


Getting Started
---------------

Clone this repo with your desired project name:

```
git clone git://github.com/rca/django-baseline.git myproject
cd myproject
scripts/bootstrap.sh
```

The bootstrap script will rename the baseline remote repo to baseline so that
origin is left open for your project.  It will also create a virtual
environment using virtualenvwrapper if it's available, otherwise in the
```venv``` directory, create a secret key file as a seed for Django's crypto
functions, create a localsettings module, which enables debug, and sync
databases for local development.


Developing your app
-------------------

Create your application:

```
django-admin.py startapp myapp
git add myapp
git commit -m'Added django app, "myapp"'
```

Application Settings
--------------------

Create ```myapp/settings.py``` and ```myapp/urls.py``` with your application's
custom settings.  Then create ```baseline/local_settings.py``` and
```baseline/local_urls.py``` to tie them into the application.

Any sensitive data, such as passwords, should not be kept in settings files
that end up in the repository but rather in environment variables.  Any
environment variable that starts with ```DJANGO_``` will be automatically added
to settings with the prefix removed.  For example, DJANGO_FOO will end up being
FOO in Django's settings.

For development, you can add these to your environment before running django,
or add the variables to your application's ```settings.py```.


Run your application
--------------------

Run your local server and access your site at http://localhost:8000/

```
python manage.py runserver
```


Happy Hacking
-------------

You're on your way.  If this is your first time diving into Django take a look
at its excellent documentation at https://docs.djangoproject.com/en/1.5/
