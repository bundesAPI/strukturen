from .base import *
from os import environ
import os

from django_secrets import SECRETS

# aws access key for secret manager and s3
AWS_ACCESS_KEY_ID = os.environ.get("APPLICATION_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("APPLICATION_AWS_SECRET_ACCESS_KEY")

AWS_SECRETS_MANAGER_SECRET_NAME = os.environ.get("AWS_SECRETS_MANAGER_SECRET_NAME")
AWS_SECRETS_MANAGER_SECRET_SECTION = os.environ.get(
    "AWS_SECRETS_MANAGER_SECRET_SECTION"
)
AWS_SECRETS_MANAGER_REGION_NAME = os.environ.get("AWS_REGION_NAME")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": SECRETS.get("RDS_DB_HOST"),
        "NAME": SECRETS.get("RDS_DB_NAME"),
        "USER": SECRETS.get("RDS_DB_USER"),
        "PASSWORD": SECRETS.get("RDS_DB_PASSWORD"),
    },
}

ALLOWED_CIDR_NETS = ["172.16.0.0/12", "127.0.0.1/8"]
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=SECRETS.get("SENTRY_DSN"),
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

SOCIAL_AUTH_JSONFIELD_ENABLED = True

# TODO
ALLOWED_HOSTS = [
    os.environ.get("ALLOWED_HOSTS"),
    ".elasticbeanstalk.com",
    ".amazonaws.com",
]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://[a-zA-z0-9-.]{1,}\.bund\.dev$",
    r"^http://127.0.0.1:[0-9]{1,}$",
    r"^http://localhost:[0-9]{1,}$",
]

AWS_EB_DEFAULT_REGION = os.environ.get("AWS_REGION_NAME")

# https://github.com/jschneier/django-storages/issues/782
AWS_S3_ADDRESSING_STYLE = "virtual"

SECRET_KEY = SECRETS.get("SECRET_KEY")

JWT_PRIVATE_KEY_STRUKTUREN = SECRETS.get("JWT_PRIVATE_KEY")
JWT_PUBLIC_KEY_STRUKTUREN = SECRETS.get("JWT_PUBLIC_KEY")

USE_TZ = False

STATIC_ROOT = "/static/"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_REGION_NAME = os.environ.get("AWS_REGION_NAME")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
OPEN_SEARCH_CLUSTER_ENDPOINT = os.environ.get("OPEN_SEARCH_CLUSTER_ENDPOINT")

ORGCHART_CRAWLER_SNS_TOPIC = os.environ.get("ORGCHART_CRAWLER_SNS_TOPIC")
ORGCHART_ANALYSIS_SNS_TOPIC = os.environ.get("ORGCHART_ANALYSIS_SNS_TOPIC")

SOCIAL_AUTH_GITHUB_KEY = SECRETS.get("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = SECRETS.get("SOCIAL_AUTH_GITHUB_SECRET")
SOCIAL_AUTH_GITHUB_SCOPE = ["user:email"]

SOCIAL_AUTH_FROIDE_KEY = SECRETS.get("SOCIAL_AUTH_FROIDE_KEY")
SOCIAL_AUTH_FROIDE_SECRET = SECRETS.get("SOCIAL_AUTH_FROIDE_SECRET")

from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection
import boto3

credentials = boto3.session.Session(
    region_name=AWS_EB_DEFAULT_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
).get_credentials()
auth = AWSV4SignerAuth(credentials, AWS_EB_DEFAULT_REGION)

OPENSEARCH_DSL = {
    "default": {
        "hosts": [{"host": OPEN_SEARCH_CLUSTER_ENDPOINT, "port": 443}],
        "http_auth": auth,
        "use_ssl": True,
        "verify_certs": True,
        "connection_class": RequestsHttpConnection,
    }
}

try:
    from .local import *
except ImportError:
    pass
