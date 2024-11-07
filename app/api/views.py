from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from loguru import logger
from .serializers import AuthParamsSerializer
from .models import AmoWidget, AmoProject
from .amo_api import get_tokens_by_code


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
        response = get_tokens_by_code(client_id, widget.client_secret, code, referer.split(".")[0])
        access_token = response.get("access_token")
        refresh_token = response.get("refresh_token")
        logger.debug(f"Получены токены {response}")
        AmoProject.objects.create(
            subdomain=referer.split(".")[0],
            access_token=access_token,
            refresh_token=refresh_token,
            widget=widget
        )
        return Response({"status": "oke"}, status=200)
    
    def post(self, request: Request):
        logger.debug(f"AmoWebhookView.data = {request.data}")
        return Response({"status": "oke"}, status=200)


class AmoWebhookView(APIView):
    
    def post(self, request: Request):
        amo = AmoProject.objects.first()
        amo_api = amo.get_api()
        me = amo_api.get_me()
        return Response(me.model_dump(), status=200)
