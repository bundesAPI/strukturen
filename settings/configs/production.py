from .base import *
from os import environ
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": environ.get("RDS_DB_HOST"),
        "NAME": environ.get("RDS_DB_NAME"),
        "USER": environ.get("RDS_DB_USER"),
        "PASSWORD": environ.get("RDS_DB_PASSWORD"),
    },
}

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS")]

CORS_ALLOW_ALL_ORIGINS = False

AWS_EB_DEFAULT_REGION = "eu-central-1"
# your aws access key id
AWS_ACCESS_KEY_ID = os.environ.get("APPLICATION_AWS_ACCESS_KEY_ID")
# your aws access key
AWS_SECRET_ACCESS_KEY = os.environ.get("APPLICATION_AWS_ACCESS_KEY_ID")
# queue name to use - queues that don't exist will be created automatically

SECRET_KEY = environ.get("DJANGO_SECRET_KEY")

JWT_PRIVATE_KEY_STRUKTUREN = environ.get("JWT_PRIVATE_KEY")
JWT_PUBLIC_KEY_STRUKTUREN = environ.get("JWT_PUBLIC_KEY")

USE_TZ = False

STATIC_ROOT = "/static/"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_REGION_NAME = "eu-central-1"
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")

try:
    from .local import *
except ImportError:
    pass
