# site/backend/app.py

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from auth import generate_google_login_url, exchange_code_for_token, get_user_info

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar a aplicação FastAPI
app = FastAPI(
    title="Zer0 Auth Site",
    description="Mini site para autenticação de usuários",
    version="1.0.0",
)

# Montar arquivos estáticos (CSS, imagens, JS, etc.)
app.mount("/static", StaticFiles(directory="../frontend/assets"), name="static")

# Configurar diretório de templates HTML
templates = Jinja2Templates(directory="../frontend")

# Rota principal - Página inicial
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota de sucesso - Após login
@app.get("/sucesso", response_class=HTMLResponse)
async def sucesso(request: Request):
    return templates.TemplateResponse("sucesso.html", {"request": request})

# Rota de login (redireciona para o Google OAuth)
@app.get("/login")
async def login(request: Request):
    login_url = generate_google_login_url()
    return RedirectResponse(url=login_url)

# Rota de callback - Google OAuth redireciona aqui
@app.get("/callback")
async def callback(request: Request, code: str = None):
    if not code:
        raise HTTPException(status_code=400, detail="Código de autenticação não fornecido.")
    
    # Trocar o código por um access token
    try:
        token_data = await exchange_code_for_token(code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao trocar o código por token: {e}")

    # Usar o access token para obter informações do usuário
    user_info = await get_user_info(token_data['access_token'])
    
    # Exibir informações do usuário ou salvar a sessão
    # Aqui você pode guardar as informações do usuário (como email) para uma sessão ou banco de dados
    return templates.TemplateResponse("sucesso.html", {"request": request, "user": user_info})

# Rota de logout
@app.get("/logout")
async def logout(request: Request):
    # Aqui você pode limpar a sessão do usuário (cookies, sessão etc.)
    return RedirectResponse(url="/")
