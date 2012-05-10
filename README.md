Django Baseline
===============

Django Baseline is a ready-made Django project that helps you deploy to Heroku and get working on your application.

Getting Started
---------------

Clone this repo and point the remote to the name baseline.  Renaming the remote
to baseline leaves origin open for your project and allows you to more easily
pull in changes from baseline.

```
git clone git://github.com/rca/django-baseline.git
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
