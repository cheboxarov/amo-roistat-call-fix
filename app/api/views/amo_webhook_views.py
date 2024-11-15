from loguru import logger
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from ..models import AmoProject
from ..services import AmoAuthService


class AmoWebhookView(APIView):
    
    def post(self, request: Request):
        logger.debug(f"AmoWebhookView.data = {request.data}")
        data = request.data.dict()
        try:
            subdomain = data.get("account[subdomain]")[0]
            lead_id = data.get("leads[note][0][note][element_id]")[0]
        except Exception as err:
            logger.error(f"validation error {err}")
            return Response({"status": "ok"}, status=200)
        try:
            amo_project = AmoProject.objects.get(subdomain=subdomain)
        except AmoProject.DoesNotExist:
            return Response({"status": "ok"}, status=200)
        AmoAuthService.update_tokens(amo_project)
        api = amo_project.get_api()
        lead = api.leads.get_by_id(int(lead_id))
        logger.debug(f"Найден лид - {lead.name}")
        return Response({"status": "ok"}, status=200)
