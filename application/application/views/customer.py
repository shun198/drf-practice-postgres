from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from application.filters import CustomerFilter
from application.models import Customer
from application.serializers.customer import CustomerSerializer
from project.settings.environment import aws_settings


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomerFilter

    @action(detail=False, methods=["post"])
    def upload_csv(self, request):
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
