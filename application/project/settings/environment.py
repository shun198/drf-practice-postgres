"""環境変数定義用のモジュール"""

from pydantic import BaseSettings


class DjangoSettings(BaseSettings):
    """Django関連の環境変数を設定するクラス"""

    SECRET_KEY: str
    ALLOWED_HOSTS: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432


class AwsSettings(BaseSettings):
    """AWS関連の環境変数を設定するクラス"""

    AWS_REGION_NAME: str = "ap-northeast-1"
    ENDPOINT_URL: str = "http://localstack:4566"
    AWS_SES_REGION_NAME: str
    AWS_SES_REGION_ENDPOINT: str
    AWS_STORAGE_BUCKET_NAME: str = "localstack"
    DEFAULT_FROM_EMAIL: str
    AWS_PROFILE: str = "localstack"


django_settings = DjangoSettings()


aws_settings = AwsSettings()
