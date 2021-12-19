"""
Django settings for settings project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-@_)sfbt%39%85=#i0-)7p04gvuu-o@a%6i@3c9tlc^-r(57&@*"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "polymorphic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "reversion",
    "django_admin_json_editor",
    "graphene_django",
    # Serious Django
    "serious_django_services",
    "serious_django_permissions",
    "oauth2_provider",
    "oauth2_provider_jwt",
    "crispy_forms",
    # cors
    "corsheaders",
    "organisation",
    "person",
    "claims",
    "orgcharts",
    "oauth",
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
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
]

AUTHENTICATION_BACKENDS = (
    "oauth.oauth_backend.OAuth2Backend",
    "django.contrib.auth.backends.ModelBackend",
    "serious_django_permissions.permissions.PermissionModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)


# Serious Django configuration
DEFAULT_GROUPS_MODULE = "settings.default_groups"

OAUTH2_PROVIDER = {
    "SCOPES": {
        "administrative-staff": "Administrative Staff",
    },
}

GRAPHENE = {
    "SCHEMA": "settings.schema.schema",
    "RELAY_CONNECTION_MAX_LIMIT": 1000,
}

ROOT_URLCONF = "settings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR.joinpath("settings/templates"))],
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

STATICFILES_DIRS = ("settings/static/",)


# TODO: move this to config
JWT_ISSUER = "STRUKTUREN"
JWT_ENABLED = True
JWT_ID_ATTRIBUTE = "email"

WSGI_APPLICATION = "settings.wsgi.application"


# claims that are used in the code
CLAIMS = {"LEADS": "leads"}

# Base url to serve media files
MEDIA_URL = "/media/"

# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, "dev_media/")


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

CORS_ALLOW_ALL_ORIGINS = True

LANGUAGE_CODE = "de-DE"

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ("en-US", _("English")),
    ("de-DE", _("German")),
)

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"