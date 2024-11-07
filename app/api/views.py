from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from loguru import logger
from .serializers import AuthParamsSerializer
from .models import AmoWidget


class AmoInstallWidgetWebhookView(APIView):

    def get(self, request: Request):
        params = request.query_params
        serializer = AuthParamsSerializer(data=params)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        code = params.get("code")
        client_id = params.get("client_id")
        referer = params.get("referer")
        widget = AmoWidget.objects.filter(client_id=client_id)
        if not widget.exists():
            logger.error(f"widget with client_id={client_id} not found")
            return Response({"status": "oke"}, status=200)
        widget = widget.first()
        return Response({"status": "oke"}, status=200)
    
    def post(self, request: Request):
        logger.debug(f"AmoWebhookView.data = {request.data}")
        return Response({"status": "oke"}, status=200)


class AmoWebhookView(APIView):
    
    def post(self, request: Request):
        logger.debug(f"AmoWebhookView.data = {request.data}")
        return Response({"status": "oke"}, status=200)
