from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from loguru import logger
from ..services import AmoAuthService
from ..serializers import AuthParamsSerializer


class AmoInstallWidgetWebhookView(APIView):

    def get(self, request: Request):
        
        params = request.query_params
        serializer = AuthParamsSerializer(data=params)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data

        AmoAuthService.install_widget(params)

        return Response({"result": "ok"}, status=200)
        
    
    def post(self, request: Request):
        logger.debug(f"AmoWebhookView.data = {request.data}")
        return Response({"status": "oke"}, status=200)