Django Baseline
===============

Django Baseline is a ready-made Django project that helps you deploy to Heroku and get working on your application.

Getting Started
---------------

Once you have cloned this repo, initialize heroku in the project directory and push to Heroku:

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
