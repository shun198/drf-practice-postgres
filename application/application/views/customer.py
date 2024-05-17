import json

import chardet
from botocore.exceptions import ClientError
from django.conf import settings
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from application.filters import CustomerFilter
from application.models import Customer
from application.serializers.customer import (
    CustomerSerializer,
    UploadCSVSerializer,
    UploadCustomerHistorySerializer,
)
from project.settings.environment import aws_settings


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomerFilter

    def get_serializer_class(self):
        match self.action:
            case "upload_csv":
                return UploadCSVSerializer
            case "register_customer":
                return None
            case _:
                return CustomerSerializer

    @action(detail=False, methods=["post"])
    def upload_csv(self, request):
        csv = request.FILES["file"]
        if not csv.name.endswith(".csv"):
            return JsonResponse(
                {"msg": "csvファイルをアップロードしてください"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            csv.read().decode("utf-8-sig")
        except BaseException:
            return JsonResponse(
                {
                    "msg": "CSVファイルのエンコードが間違っています。utf-8に指定してください"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = UploadCustomerHistorySerializer(data={"csv": csv})
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        msg = {
            "csv": csv.name,
        }
        try:
            settings.BOTO3_SQS_CLIENT.send_message(
                QueueUrl=aws_settings.AWS_SQS_URL,
                MessageBody=json.dumps(msg),
                MessageGroupId=aws_settings.AWS_SQS_MESSAGE_GROUP,
            )
        except ClientError as e:
            print(e)
            return JsonResponse(
                {"msg": "CSVファイルのアップロードに失敗"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return JsonResponse(
            {
                "msg": "CSVファイルのアップロードに成功しました",
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def register_customer(self, request):
        if request.data.get("token", "") != aws_settings.LAMBDA_TOKEN:
            # 攻撃者へ情報を与えない為にレスポンスにメッセージを入れない
            return JsonResponse(
                data={"msg": ""},
                status=status.HTTP_400_BAD_REQUEST,
            )
        csv = request.data.get("csv")
        with csv.open():
            encoding = chardet.detect(csv.read())
            if encoding["encoding"] != "utf-8":
                raise Exception(
                    "utf-8にエンコードされたCSVファイルを指定してください"
                )
            csv.seek(0)
            data = csv.read().decode()
        return JsonResponse(
            {
                "msg": "お客様情報の登録が完了しました",
            },
            status=status.HTTP_201_CREATED,
        )
