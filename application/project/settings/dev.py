"""DEV環境用の設定"""

from logging.config import dictConfig

import boto3

from application.injectors import DevModule, injector
from application.utils.logs import ConfFile

from .base import *
from .environment import aws_settings

DEBUG = False
ROOT_URLCONF = "project.urls.base"

INSTALLED_APPS += [
    "django_ses",
    "storages",
]


# SESの設定
EMAIL_BACKEND = "django_ses.SESBackend"
AWS_SES_REGION_NAME = aws_settings.AWS_DEFAULT_REGION_NAME
AWS_SES_REGION_ENDPOINT = aws_settings.AWS_SES_REGION_ENDPOINT
DEFAULT_FROM_EMAIL = aws_settings.DEFAULT_FROM_EMAIL
# S3の設定
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
AWS_STORAGE_BUCKET_NAME = aws_settings.AWS_STORAGE_BUCKET_NAME

BOTO3_SQS_CLIENT = boto3.client(
    "sqs",
    endpoint_url=aws_settings.ENDPOINT_URL,
    region_name=aws_settings.AWS_DEFAULT_REGION_NAME,
)

# ログ設定
dictConfig(ConfFile.get()["dev"]["logging"])

# DI設定
injector.binder.install(DevModule())
