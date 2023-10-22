"""
Django settings for bltestproject project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from baseline.settings import *

ROOT_URLCONF = "bltestproject.urls"
WSGI_APPLICATION = "bltestproject.wsgi.application"


if BASELINE_TEST_APP not in INSTALLED_APPS:
    INSTALLED_APPS += [BASELINE_TEST_APP]

# for tests to run
INSTALLED_APPS += [
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_email",  # <- if you want email capability.
    "two_factor",
    # "two_factor.plugins.phonenumber",  # <- if you want phone number capability.
    "two_factor.plugins.email",  # <- if you want email capability.
    # 'two_factor.plugins.yubikey',  # <- for yubikey capability.
]
