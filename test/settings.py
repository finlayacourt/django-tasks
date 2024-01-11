# pyright: reportConstantRedefinition=none

from pathlib import Path
from typing import Any

import django_stubs_ext

BASE_DIR = Path(__file__).resolve().parent.parent


# Monkeypatching Django, so stubs will work for all generics
# https://github.com/typeddjango/django-stubs

django_stubs_ext.monkeypatch()

DEBUG = True

SECRET_KEY = "d9zWbQynRVY6xCP5kY93uGySre80J4SiOQWYTnAkkMGyuR75dg"

ALLOWED_HOSTS = [
    ".localhost",
    "0.0.0.0",
    "127.0.0.1",
    "[::1]",
]

INSTALLED_APPS: tuple[str, ...] = (
    "test",
    "tasks",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
)

MIDDLEWARE: tuple[str, ...] = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "test.urls"

WSGI_APPLICATION = "test.wsgi.application"

# Static Files
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

TIME_ZONE = "UTC"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "scheduler",
        "USER": "scheduler",
        "PASSWORD": "scheduler",
        "HOST": "localhost",
        "PORT": 5432,
    },
}

# Templates
# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-TEMPLATES

TEMPLATES: list[dict[str, Any]] = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]
