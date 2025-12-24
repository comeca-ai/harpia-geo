"""
🧪 Tool de Teste de Visibilidade em LLMs
"""

import os
import asyncio
from agents import function_tool
from openai import AsyncOpenAI
import google.generativeai as genai


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


@function_tool
async def testar_visibilidade_llm(
    empresa: str,
    prompts: list,
    llms: list = None
) -> dict:
    """
    Testa se a empresa é mencionada nas respostas das LLMs.

    Args:
        empresa: Nome da empresa para buscar nas respostas
        prompts: Lista de prompts para testar (usa os 5 primeiros)
        llms: Lista de LLMs para testar (default: ["chatgpt", "gemini"])

    Returns:
        Resultados do teste com score de visibilidade
    """
    if llms is None:
        llms = ["chatgpt", "gemini"]

    # Usa apenas os primeiros 5 prompts para economizar
    prompts_teste = prompts[:5]

    resultados = {
        "empresa": empresa,
        "total_prompts_testados": len(prompts_teste),
        "llms_testadas": llms,
        "resultados_por_llm": {},
        "score_geral": 0,
        "detalhes": []
    }

    total_mencoes = 0
    total_testes = 0

    for llm in llms:
        llm_resultados = []
        mencoes_llm = 0

        for prompt in prompts_teste:
            prompt_texto = prompt.get("texto", prompt) if isinstance(prompt, dict) else prompt

            try:
                if llm == "chatgpt":
                    resposta = await testar_chatgpt(prompt_texto)
                elif llm == "gemini":
                    resposta = await testar_gemini(prompt_texto)
                else:
                    resposta = "LLM não suportada"

                # Verifica se a empresa foi mencionada
                mencionado = empresa.lower() in resposta.lower()

                if mencionado:
                    mencoes_llm += 1
                    total_mencoes += 1

                llm_resultados.append({
                    "prompt": prompt_texto[:100] + "..." if len(prompt_texto) > 100 else prompt_texto,
                    "mencionado": mencionado,
                    "resposta_preview": resposta[:200] + "..." if len(resposta) > 200 else resposta
                })

                total_testes += 1

            except Exception as e:
                llm_resultados.append({
                    "prompt": prompt_texto[:100],
                    "mencionado": False,
                    "erro": str(e)
                })
                total_testes += 1

        # Calcula score da LLM
        score_llm = (mencoes_llm / len(prompts_teste)) * 100 if prompts_teste else 0

        resultados["resultados_por_llm"][llm] = {
            "mencoes": mencoes_llm,
            "total": len(prompts_teste),
            "score": round(score_llm, 1),
            "detalhes": llm_resultados
        }

    # Score geral
    resultados["score_geral"] = round((total_mencoes / total_testes) * 100, 1) if total_testes > 0 else 0

    # Classificação
    if resultados["score_geral"] >= 80:
        resultados["classificacao"] = "excelente"
        resultados["emoji"] = "🟢"
        resultados["mensagem"] = "Parabéns! Sua empresa tem ótima visibilidade nas IAs."
    elif resultados["score_geral"] >= 50:
        resultados["classificacao"] = "bom"
        resultados["emoji"] = "🟡"
        resultados["mensagem"] = "Sua empresa aparece em algumas buscas, mas pode melhorar."
    elif resultados["score_geral"] >= 20:
        resultados["classificacao"] = "regular"
        resultados["emoji"] = "🟠"
        resultados["mensagem"] = "Sua visibilidade está baixa. Hora de otimizar!"
    else:
        resultados["classificacao"] = "critico"
        resultados["emoji"] = "🔴"
        resultados["mensagem"] = "As IAs não conhecem sua empresa. Precisamos mudar isso!"

    return resultados


async def testar_chatgpt(prompt: str) -> str:
    """
    Testa um prompt no ChatGPT.
    """
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    response = await client.chat.completions.create(
        model="gpt-4o-mini",  # Usa modelo mais barato para testes
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )

    return response.choices[0].message.content


async def testar_gemini(prompt: str) -> str:
    """
    Testa um prompt no Google Gemini.
    """
    if not GOOGLE_API_KEY:
        return "API Key do Gemini não configurada"

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    response = await asyncio.to_thread(
        model.generate_content,
        prompt
    )

    return response.text


async def testar_perplexity(prompt: str) -> str:
    """
    Testa um prompt no Perplexity (futuro).
    """
    # TODO: Implementar quando tivermos API
    return "Perplexity não implementado ainda"
