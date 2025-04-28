# site/backend/auth.py

import os
import httpx
from urllib.parse import urlencode

# Variáveis do .env
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# URLs importantes
GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"

# Escopos que queremos acessar do Google
GOOGLE_SCOPES = [
    "openid",
    "email",
    "profile",
]


def generate_google_login_url():
    """Gera a URL para o usuário ser redirecionado e fazer login pelo Google."""
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(GOOGLE_SCOPES),
        "access_type": "offline",
        "prompt": "consent",  # Sempre pedir consentimento para novo refresh_token
    }
    return f"{GOOGLE_AUTH_ENDPOINT}?{urlencode(params)}"


async def exchange_code_for_token(code: str):
    """Troca o authorization code pelo access token."""
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_TOKEN_ENDPOINT, data=data)
        response.raise_for_status()
        return response.json()


async def get_user_info(access_token: str):
    """Obtém informações do usuário autenticado usando o access token."""
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_USERINFO_ENDPOINT, headers=headers)
        response.raise_for_status()
        return response.json()
