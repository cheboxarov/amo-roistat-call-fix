from ..models import AmoProject, AmoWidget
from loguru import logger
from rest_framework.exceptions import APIException
from .amo_api import get_tokens_by_code


class AmoAuthService:

    @staticmethod
    def install_widget(params: dict) -> AmoProject:
        """
        На основе параметров вебхука получает аксесс и рефреш токены проекта
        """
        code = params.get("code")
        client_id = params.get("client_id")
        referer = params.get("referer")
        subdomain = referer.split(".")[0]

        widget = AmoWidget.objects.filter(client_id=client_id)
        if not widget.exists():
            logger.error(f"widget with client_id={client_id} not found")
            raise APIException(detail="widget not found", code=200)
        widget = widget.first()

        response = get_tokens_by_code(client_id, widget.client_secret, code, subdomain)
        access_token = response.get("access_token")
        refresh_token = response.get("refresh_token")
        return AmoProject.objects.create(
            subdomain=subdomain,
            access_token=access_token,
            refresh_token=refresh_token,
            widget=widget
        )