"""
🦅 HARPIA - GEO Platform
Backend FastAPI + ChatKit Server
"""

import os
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from chatkit.server import ChatKitServer, StreamingResult
from chatkit.store import InMemoryStore

from agents.harpia_agent import HarpiaAgent
from store.supabase_store import SupabaseStore


# Configuração
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
USE_SUPABASE = SUPABASE_URL and SUPABASE_KEY


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa recursos do app."""
    print("🦅 Harpia iniciando...")
    yield
    print("🦅 Harpia encerrando...")


app = FastAPI(
    title="Harpia GEO Platform",
    description="Plataforma de Generative Engine Optimization",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store - usa Supabase em produção, InMemory em dev
if USE_SUPABASE:
    store = SupabaseStore(SUPABASE_URL, SUPABASE_KEY)
else:
    store = InMemoryStore()

# ChatKit Server com Agent Harpia
harpia_server = HarpiaAgent(store=store)


@app.get("/")
async def root():
    """Health check."""
    return {
        "status": "ok",
        "service": "Harpia GEO Platform",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check detalhado."""
    return {
        "status": "healthy",
        "store": "supabase" if USE_SUPABASE else "memory",
        "openai": bool(OPENAI_API_KEY)
    }


@app.post("/api/session")
async def create_session(request: Request):
    """
    Cria uma nova sessão ChatKit.
    Retorna o client_secret para o frontend.
    """
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)

    # Cria sessão ChatKit
    session = client.chat.sessions.create(
        model="gpt-4.1",
        metadata={"platform": "harpia"}
    )

    return {
        "client_secret": session.client_secret,
        "session_id": session.id
    }


@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    """
    Endpoint principal do ChatKit.
    Processa mensagens e retorna stream de eventos.
    """
    body = await request.body()
    context = {
        "headers": dict(request.headers),
        "client_ip": request.client.host if request.client else None
    }

    result = await harpia_server.process(body, context=context)

    if isinstance(result, StreamingResult):
        return StreamingResponse(
            result,
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )

    return Response(
        content=result.json,
        media_type="application/json"
    )


@app.post("/api/diagnostico")
async def diagnostico_direto(request: Request):
    """
    Endpoint direto para diagnóstico (sem chat).
    Útil para integrações e testes.
    """
    data = await request.json()
    empresa = data.get("empresa")
    site = data.get("site")

    if not empresa or not site:
        return {"error": "empresa e site são obrigatórios"}

    from tools.diagnostico import diagnostico_empresa
    from tools.prompts import gerar_prompts

    # Executa diagnóstico
    dados = await diagnostico_empresa(empresa, site)

    # Gera prompts
    prompts = await gerar_prompts(empresa, dados)

    return {
        "empresa": empresa,
        "site": site,
        "dados": dados,
        "prompts": prompts,
        "total_prompts": len(prompts)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
