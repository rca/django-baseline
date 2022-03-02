"""
Django settings for webproject project.

Generated by 'django-admin startproject' using Django 3.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

import conversion
import dj_database_url

from .utils import get_setting, is_test

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_setting("DJANGO_SECRET_KEY", maintenance_default="super-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = conversion.convert_bool(get_setting("DJANGO_DEBUG", default="False"))

ALLOWED_HOSTS = conversion.convert_list(
    get_setting("DJANGO_ALLOWED_HOSTS", default="", maintenance_default="*")
)

CORS_ALLOWED_ORIGINS = conversion.convert_list(
    get_setting("CORS_ALLOWED_ORIGINS", default="")
)

# pypy compatibility
PYPY_ENABLE_COMPAT = conversion.convert_bool(
    get_setting("PYPY_ENABLE_COMPAT", default="false")
)
if PYPY_ENABLE_COMPAT:
    from psycopg2cffi import compat

    compat.register()

# Application definition

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "postgresql_setrole",
    "rest_framework",
    "baseline",
    "roles",
]

BASELINE_TEST_APP = "bltestapp"
if is_test():
    INSTALLED_APPS += [
        BASELINE_TEST_APP,
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "webproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "webproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASE_URL = get_setting("DATABASE_URL")
database = dj_database_url.config(default=DATABASE_URL)
if not database:
    raise ValueError("no database found")

# set the role per the env
POSTGRES_SET_ROLE = get_setting("POSTGRES_SET_ROLE", required=False)
if POSTGRES_SET_ROLE:
    database["SET_ROLE"] = POSTGRES_SET_ROLE

DATABASES = {"default": database}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "baseline.permissions.FullDjangoModelPermissions",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "baseline.renderers.EnvelopeJSONRenderer",
    ],
    "PAGE_SIZE": 100,
}

TRAILING_SLASH = get_setting("TRAILING_SLASH", default=False)
