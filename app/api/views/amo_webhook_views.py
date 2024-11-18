from loguru import logger
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from ..models import AmoProject
from ..services import AmoAuthService


class AmoWebhookView(APIView):
    
    def post(self, request: Request):
        data = request.data.dict()
        try:
            subdomain = data.get("account[subdomain]")
            lead_id = data.get("leads[note][0][note][element_id]")
            note_id = data.get("leads[note][0][note][note_type]")
            created_by = data.get("leads[note][0][note][created_by]")

            logger.debug(f"subdomain - {subdomain}\nlead_id - {lead_id}\nnote_id - {note_id}\ncreated_by - {created_by}")
        except Exception as err:
            logger.error(f"validation error {err}")
            return Response({"status": "ok"}, status=200)
        try:
            amo_project = AmoProject.objects.get(subdomain=subdomain)
        except AmoProject.DoesNotExist:
            logger.error(f"Amo project not found")
            return Response({"status": "ok"}, status=200)
        try:
            AmoAuthService.update_tokens(amo_project)
            api = amo_project.get_api()
            lead = api.leads.get_by_id(int(lead_id))
            logger.debug(f"\nНайден лид - {lead.name}\nnote_id = {note_id}\ncreated_by = {created_by}\n")
        except Exception as error:
            logger.error(f"error for get lead - {error}")
        finally:
            return Response({"status": "ok"}, status=200)
