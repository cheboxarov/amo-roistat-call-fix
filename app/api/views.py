from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from loguru import logger


class AmoInstallWidgetWebhookView(APIView):
    
    def post(self, request: Request):
        logger.debug(f"AmoWebhookView.data = {request.data}")
        return Response({"status": "oke"}, status=200)


class AmoWebhookView(APIView):
    
    def post(self, request: Request):
        logger.debug(f"AmoWebhookView.data = {request.data}")
        return Response({"status": "oke"}, status=200)
