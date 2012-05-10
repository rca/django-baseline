Django Baseline
===============

Django Baseline is a ready-made Django project that helps you deploy to Heroku and get working on your application.

Getting Started
---------------

Clone this repo and point the remote to the name baseline.  Renaming the remote
to baseline leaves origin open for your project and allows you to more easily
pull in changes from baseline.

```
git clone git://github.com/rca/django-baseline.git myproject
cd myproject
git remote rename origin baseline
```

Next, generate a secret key for django to use for crypto functions:

```
python manage.py secretkey
git add baseline/secretkey.py
git commit -m'Added secret key module'
```

Then, initialize heroku in the project directory and push to Heroku:

```
heroku create --stack cedar
git push heroku master
```

Once the application is running on Heroku, sync the database:

```
heroku run python manage.py syncdb
heroku run python manage.py migrate
```

And finally, to see your application:

```
heroku open
```

Developing your app
-------------------

First, create a virtual environment and populate it with the requirements:

```
virtualenv venv --distribute
source venv/bin/activate
pip install -r requirements.txt
```

Create ```baseline/localsettings.py``` with ```DEBUG``` configured:

```
echo "DEBUG = True" >> baseline/localsettings.py
```

Sync the database:

```
python manage.py syncdb
python manage.py migrate
```

Start your application and tie in its urls.  The localurls command creates
```baseline/localurls.py``` that's automatically imported and ties in your
application's ```urls.py``` file.

```
django-admin.py startapp myapp
git add myapp
git commit -m'Added django app, "myapp"'

python manage.py localurls myapp
```

Now run a server locally and access your site at http://localhost:8000/

```
python manage.py runserver
```

This would be a good time to commit all the files the commands above generated:

```
git add -A
git commit -m'Added baseline-generated commands'
```

Happy Hacking
-------------

You're on your way.  If this is your first time diving into Django take a look
at its excellent documentation at https://docs.djangoproject.com/en/1.4/
