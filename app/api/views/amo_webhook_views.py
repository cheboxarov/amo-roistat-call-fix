from loguru import logger
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from ..models import AmoProject, LeadProcessed
from ..services import AmoAuthService
import time


class AmoWebhookView(APIView):
    
    def post(self, request: Request):
        data = request.data.dict()
        logger.debug(f"wh data: {data}")
        try:
            subdomain = data.get("account[subdomain]")
            lead_id = data.get("leads[note][0][note][element_id]")
            note_id = data.get("leads[note][0][note][note_type]")
            created_by = data.get("leads[note][0][note][created_by]")
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
            lead = api.leads.get_by_id(int(lead_id), with_="contacts")
            logger.debug(f"\nНайден лид - {lead}\nnote_id = {note_id}\ncreated_by = {created_by}\n")
            # if not int(lead.created_at / 100) == int(time.time() / 100):
            #     logger.debug(f"Слишком давно создан")
            #     return Response({"status": "ok"}, status=200)

            logger.debug(f"Сделка создана: {lead.created_at} Сейчас {time.time()} Разница во времени {int(lead.created_at / 100) - int(time.time() / 100)}")
            
            if int(note_id) == 10 and not LeadProcessed.objects.filter(lead_id=lead_id).exists():
                lead.responsible_user_id = created_by
                api.leads.update(lead)
                for contact in lead.embedded.get("contacts"):
                    if contact.get("is_main"):
                        contact_id = contact.get("id")
                        contact = api.contacts.get_by_id(contact_id)
                        contact.responsible_user_id = created_by
                        api.contacts.update(contact)
                LeadProcessed.objects.create(lead_id=lead_id)
        except Exception as error:
            logger.error(f"error for get lead - {error}")
        finally:
            return Response({"status": "ok"}, status=200)
