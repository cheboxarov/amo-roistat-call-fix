import requests


def get_tokens_by_code(client_id: str, client_secret: str, code: str, subdomain: str) -> dict[str, str]:
    url = f"https://{subdomain}.amocrm.ru/oauth2/access_token"
    body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://apps.widgets-tema.ru/amo-roistat-fix/install/"
    }
    response = requests.post(url, json=body)
    response.raise_for_status()
    return response.json()

