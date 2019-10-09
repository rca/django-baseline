# Django Baseline

Django Baseline is a ready-made Django project to eliminate the boilerplate.


## Getting Started

This project uses Docker + Docker Compose + Compose Flow as the development dependencies.

Clone this repo with your desired project name:

```
git clone git://github.com/rca/django-baseline.git myproject
cd myproject
pipenv shell
pipenv install --dev
compose-flow -e local task bootstrap
```

The bootstrap script will rename the baseline remote repo to baseline so that
origin is left open for your project.  It will also create a virtual
environment using pipenv.  The `pipenv install --dev` command will install all the packages needed to run the `compose-flow` command.


## Developing your app

This project is configured to be Docker-based.  All development can be done without installing anything locally.  Django can be run in the Docker container using the command:

```
compose-flow -e local compose run --rm app /bin/bash
```

Once you're in a shell, your local environment is the same as your deployment environment in the container.  From there, run Django commands as usual; to start, create an app:

```
./manage.py startapp myapp
```


## Application Settings

Create `myapp/settings.py` and `myapp/urls.py` with your application's
custom settings.  Then create `baseline/local_settings.py` and
`baseline/local_urls.py` to tie them into the application.

Any sensitive data, such as passwords, should not be kept in settings files
that end up in the repository but rather in environment variables.


## Run your application

Run your local server and access your site at http://localhost:8000/.  The following command will start a postgres container and serve the Django app using runserver

```
compose-flow -e local compose up
```

In another shell you can exec into the running container:

```
compose-flow -e local compose exec app /bin/bash
```


## Happy Hacking

You're on your way.  If this is your first time diving into Django take a look
at its excellent documentation at https://docs.djangoproject.com/
