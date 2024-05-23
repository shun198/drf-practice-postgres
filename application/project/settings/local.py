"""LOCAL環境用の設定"""

from logging.config import dictConfig

import boto3

from application.injectors import LocalModule, injector
from application.utils.logs import ConfFile
from project.settings.environment import aws_settings

from .base import *

DEBUG = True

REST_FRAMEWORK.update(
    {"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"}
)

SPECTACULAR_SETTINGS = {
    "TITLE": "プロジェクト名",
    "DESCRIPTION": "詳細",
    "VERSION": "1.0.0",
}

INSTALLED_APPS += [
    "debug_toolbar",
    "drf_spectacular",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "project.urls.local"

# Djangoのメールの設定
EMAIL_HOST = "mail"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
# SMTPの1025番ポートを指定
EMAIL_PORT = 1025
# 送信中の文章の暗号化をFalseにします
EMAIL_USE_TLS = False

# DI設定
injector.binder.install(LocalModule())

AWS_ACCESS_KEY_ID = "localstack"
AWS_SECRET_ACCESS_KEY = "localstack"
AWS_S3_ENDPOINT_URL = aws_settings.AWS_S3_ENDPOINT

BOTO3_CLIENT_S3 = boto3.client(
    "s3",
    aws_access_key_id="",
    aws_secret_access_key="",
    endpoint_url=AWS_S3_ENDPOINT_URL,
    region_name=aws_settings.AWS_DEFAULT_REGION_NAME,
)

BOTO3_SQS_CLIENT = boto3.client(
    "sqs",
    endpoint_url=aws_settings.ENDPOINT_URL,
    aws_access_key_id="localstack",
    aws_secret_access_key="localstack",
    region_name=aws_settings.AWS_DEFAULT_REGION_NAME,
)

# ログ設定
output_path = Path("output")
if not output_path.exists():
    output_path.mkdir()
dictConfig(ConfFile.get()["local"]["logging"])
