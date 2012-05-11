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

Happy Hacking
-------------

You're on your way.  If this is your first time diving into Django take a look
at its excellent documentation at https://docs.djangoproject.com/en/1.4/
