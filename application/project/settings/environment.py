"""環境変数定義用のモジュール"""

from pydantic import BaseSettings


class DjangoSettings(BaseSettings):
    """Django関連の環境変数を設定するクラス"""

    SECRET_KEY: str = "django"
    ALLOWED_HOSTS: str = "localhost 127.0.0.1 [::1]"
    POSTGRES_NAME: str = "django"
    POSTGRES_USER: str = "django"
    POSTGRES_PASSWORD: str = "django"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432


class AwsSettings(BaseSettings):
    """AWS関連の環境変数を設定するクラス"""

    ENDPOINT_URL: str = "http://localstack:4566"
    AWS_DEFAULT_REGION_NAME: str = "ap-northeast-1"
    AWS_SES_REGION_ENDPOINT: str = "email.ap-northeast-1.amazonaws.com"
    AWS_S3_ENDPOINT: str = "http://localstack:4566"
    AWS_STORAGE_BUCKET_NAME: str = "localstack"
    DEFAULT_FROM_EMAIL: str = "django@example.com"
    AWS_SQS_URL: str = "http://sqs.ap-northeast-1.localhost.localstack.cloud:4566/000000000000/queue01.fifo"
    AWS_SQS_MESSAGE_GROUP: str = "localstack"
    LAMBDA_TOKEN: str = "test"


django_settings = DjangoSettings()


aws_settings = AwsSettings()
