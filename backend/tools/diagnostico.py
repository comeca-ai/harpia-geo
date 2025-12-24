"""
🔍 Tool de Diagnóstico - Analisa empresa e site
"""

import os
import httpx
from agents import function_tool
from typing import Optional


FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # Para web search


@function_tool
async def diagnostico_empresa(
    empresa: str,
    site: str,
    nicho: Optional[str] = None
) -> dict:
    """
    Analisa o site da empresa e extrai informações para otimização GEO.

    Args:
        empresa: Nome da empresa (ex: "Datarisk")
        site: URL do site (ex: "datarisk.io" ou "https://datarisk.io")
        nicho: Nicho opcional (ex: "fintech", "saas")

    Returns:
        Dados extraídos do site e contexto da web
    """
    # Normaliza URL
    if not site.startswith("http"):
        site = f"https://{site}"

    resultado = {
        "empresa": empresa,
        "site": site,
        "nicho": nicho,
        "descricao": None,
        "servicos": [],
        "diferenciais": [],
        "publico_alvo": None,
        "contexto_mercado": None,
        "concorrentes": [],
        "erro": None
    }

    try:
        # 1. Scrape do site com Firecrawl
        site_data = await scrape_site(site)

        if site_data:
            resultado["descricao"] = site_data.get("description", "")
            resultado["servicos"] = site_data.get("services", [])
            resultado["diferenciais"] = site_data.get("differentials", [])
            resultado["publico_alvo"] = site_data.get("target_audience", "")

        # 2. Busca contexto na web
        contexto = await search_web(f"{empresa} {nicho or ''} Brasil")

        if contexto:
            resultado["contexto_mercado"] = contexto.get("summary", "")
            resultado["concorrentes"] = contexto.get("competitors", [])

    except Exception as e:
        resultado["erro"] = str(e)

    return resultado


async def scrape_site(url: str) -> dict:
    """
    Faz scrape do site usando Firecrawl API.
    """
    if not FIRECRAWL_API_KEY:
        # Fallback: scrape básico
        return await scrape_basico(url)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.firecrawl.dev/v1/scrape",
            headers={
                "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "url": url,
                "formats": ["markdown", "extract"],
                "extract": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "services": {"type": "array", "items": {"type": "string"}},
                            "differentials": {"type": "array", "items": {"type": "string"}},
                            "target_audience": {"type": "string"}
                        }
                    }
                }
            },
            timeout=30.0
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("extract", {})

        return {}


async def scrape_basico(url: str) -> dict:
    """
    Scrape básico sem Firecrawl (fallback).
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0, follow_redirects=True)

            if response.status_code == 200:
                html = response.text

                # Extrai título
                import re
                title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
                title = title_match.group(1) if title_match else ""

                # Extrai meta description
                desc_match = re.search(
                    r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
                    html,
                    re.IGNORECASE
                )
                description = desc_match.group(1) if desc_match else title

                return {
                    "description": description,
                    "services": [],
                    "differentials": [],
                    "target_audience": ""
                }
        except Exception:
            pass

    return {}


async def search_web(query: str) -> dict:
    """
    Busca informações na web usando Serper API.
    """
    if not SERPER_API_KEY:
        return {}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "q": query,
                "gl": "br",
                "hl": "pt-br",
                "num": 10
            },
            timeout=10.0
        )

        if response.status_code == 200:
            data = response.json()

            # Extrai informações relevantes
            organic = data.get("organic", [])

            return {
                "summary": " ".join([r.get("snippet", "") for r in organic[:3]]),
                "competitors": [r.get("title", "") for r in organic[:5]]
            }

    return {}
