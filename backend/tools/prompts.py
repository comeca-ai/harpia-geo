"""
📝 Tool de Geração de Prompts GEO
"""

import os
import json
from agents import function_tool
from openai import AsyncOpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


PROMPT_GENERATOR_SYSTEM = """
Você é um especialista em GEO (Generative Engine Optimization).
Sua tarefa é gerar 20 prompts otimizados que um usuário real digitaria em ChatGPT, Gemini ou Perplexity.

## Regras IMPORTANTES:

1. Cada prompt deve parecer uma busca REAL de usuário
2. Use linguagem natural em português brasileiro
3. Inclua contexto específico do nicho da empresa
4. Varie os formatos: perguntas, comandos, comparações

## Categorias (exatamente 20 prompts):

### BRANDED (5 prompts) - Mencionam a marca
- Reviews e opiniões sobre a empresa
- Como funciona o serviço X da empresa
- Cases e resultados da empresa

### UNBRANDED (5 prompts) - Problema genérico do nicho
- "Como fazer X sem Y"
- "Qual a melhor forma de Z"
- Não menciona nenhuma marca

### PROBLEM (4 prompts) - Dor específica do cliente
- Frustração real do público-alvo
- Problema que a empresa resolve
- Tom de quem precisa de ajuda

### COMPARISON (3 prompts) - Comparativos
- "X vs Y qual melhor"
- "Diferença entre X e Y"
- "Alternativas a X"

### PURCHASE (2 prompts) - Intenção de compra
- "Melhor empresa de X em [cidade]"
- "Quanto custa X"
- "Vale a pena contratar X"

### RESEARCH (1 prompt) - Pesquisa educacional
- "O que é X"
- "Como funciona X"
- Tom de quem está aprendendo

## Formato de Saída (JSON):

```json
{
  "prompts": [
    {
      "ordem": 1,
      "texto": "O prompt aqui",
      "categoria": "BRANDED",
      "intent": "informacional",
      "persona": "gerente de marketing em e-commerce",
      "formato_esperado": "lista"
    }
  ]
}
```

## Campos:
- ordem: 1-20
- texto: o prompt em si
- categoria: BRANDED, UNBRANDED, PROBLEM, COMPARISON, PURCHASE, RESEARCH
- intent: informacional, transacional, navegacional
- persona: quem faria essa busca
- formato_esperado: lista, explicacao, comparativo, guia, recomendacao
"""


@function_tool
async def gerar_prompts(
    empresa: str,
    dados: dict
) -> list:
    """
    Gera 20 prompts GEO otimizados para a empresa.

    Args:
        empresa: Nome da empresa
        dados: Dados do diagnóstico (descrição, serviços, nicho, etc)

    Returns:
        Lista de 20 prompts categorizados
    """
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    # Monta contexto da empresa
    contexto = f"""
    EMPRESA: {empresa}
    SITE: {dados.get('site', '')}
    NICHO: {dados.get('nicho', 'não especificado')}
    DESCRIÇÃO: {dados.get('descricao', '')}
    SERVIÇOS: {', '.join(dados.get('servicos', []))}
    DIFERENCIAIS: {', '.join(dados.get('diferenciais', []))}
    PÚBLICO-ALVO: {dados.get('publico_alvo', '')}
    CONTEXTO DE MERCADO: {dados.get('contexto_mercado', '')}
    CONCORRENTES: {', '.join(dados.get('concorrentes', []))}
    """

    response = await client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": PROMPT_GENERATOR_SYSTEM},
            {"role": "user", "content": f"Gere 20 prompts GEO para:\n\n{contexto}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.7
    )

    try:
        result = json.loads(response.choices[0].message.content)
        prompts = result.get("prompts", [])

        # Valida estrutura
        prompts_validados = []
        for p in prompts:
            prompts_validados.append({
                "ordem": p.get("ordem", len(prompts_validados) + 1),
                "texto": p.get("texto", ""),
                "categoria": p.get("categoria", "UNBRANDED"),
                "intent": p.get("intent", "informacional"),
                "persona": p.get("persona", ""),
                "formato_esperado": p.get("formato_esperado", "explicacao")
            })

        return prompts_validados

    except json.JSONDecodeError:
        # Fallback: retorna prompts genéricos
        return gerar_prompts_fallback(empresa, dados)


def gerar_prompts_fallback(empresa: str, dados: dict) -> list:
    """
    Gera prompts básicos caso a API falhe.
    """
    nicho = dados.get("nicho", "serviços")

    return [
        # BRANDED
        {"ordem": 1, "texto": f"{empresa} é confiável?", "categoria": "BRANDED", "intent": "informacional", "persona": "potencial cliente", "formato_esperado": "explicacao"},
        {"ordem": 2, "texto": f"Review {empresa} 2025", "categoria": "BRANDED", "intent": "informacional", "persona": "pesquisador", "formato_esperado": "lista"},
        {"ordem": 3, "texto": f"Como funciona o {empresa}?", "categoria": "BRANDED", "intent": "informacional", "persona": "curioso", "formato_esperado": "guia"},
        {"ordem": 4, "texto": f"{empresa} vale a pena?", "categoria": "BRANDED", "intent": "transacional", "persona": "decisor", "formato_esperado": "recomendacao"},
        {"ordem": 5, "texto": f"Cases de sucesso {empresa}", "categoria": "BRANDED", "intent": "informacional", "persona": "analista", "formato_esperado": "lista"},

        # UNBRANDED
        {"ordem": 6, "texto": f"Como melhorar {nicho} na minha empresa", "categoria": "UNBRANDED", "intent": "informacional", "persona": "gestor", "formato_esperado": "guia"},
        {"ordem": 7, "texto": f"Melhores práticas de {nicho}", "categoria": "UNBRANDED", "intent": "informacional", "persona": "profissional", "formato_esperado": "lista"},
        {"ordem": 8, "texto": f"Tendências de {nicho} 2025", "categoria": "UNBRANDED", "intent": "informacional", "persona": "estrategista", "formato_esperado": "lista"},
        {"ordem": 9, "texto": f"Como escolher empresa de {nicho}", "categoria": "UNBRANDED", "intent": "informacional", "persona": "comprador", "formato_esperado": "guia"},
        {"ordem": 10, "texto": f"Quanto custa {nicho} para empresas", "categoria": "UNBRANDED", "intent": "transacional", "persona": "financeiro", "formato_esperado": "explicacao"},

        # PROBLEM
        {"ordem": 11, "texto": f"Minha empresa não aparece no Google, o que fazer?", "categoria": "PROBLEM", "intent": "informacional", "persona": "empresário frustrado", "formato_esperado": "guia"},
        {"ordem": 12, "texto": f"Ninguém encontra minha empresa na internet", "categoria": "PROBLEM", "intent": "informacional", "persona": "dono de negócio", "formato_esperado": "guia"},
        {"ordem": 13, "texto": f"Como ser encontrado por clientes online", "categoria": "PROBLEM", "intent": "informacional", "persona": "empreendedor", "formato_esperado": "lista"},
        {"ordem": 14, "texto": f"Por que meus concorrentes aparecem e eu não", "categoria": "PROBLEM", "intent": "informacional", "persona": "gestor preocupado", "formato_esperado": "explicacao"},

        # COMPARISON
        {"ordem": 15, "texto": f"SEO vs GEO qual a diferença", "categoria": "COMPARISON", "intent": "informacional", "persona": "marketeiro", "formato_esperado": "comparativo"},
        {"ordem": 16, "texto": f"Melhor ferramenta de {nicho} Brasil", "categoria": "COMPARISON", "intent": "transacional", "persona": "comprador", "formato_esperado": "lista"},
        {"ordem": 17, "texto": f"{empresa} vs concorrentes", "categoria": "COMPARISON", "intent": "informacional", "persona": "analista", "formato_esperado": "comparativo"},

        # PURCHASE
        {"ordem": 18, "texto": f"Melhor empresa de {nicho} em São Paulo", "categoria": "PURCHASE", "intent": "transacional", "persona": "comprador", "formato_esperado": "recomendacao"},
        {"ordem": 19, "texto": f"Contratar {nicho} quanto custa", "categoria": "PURCHASE", "intent": "transacional", "persona": "decisor", "formato_esperado": "explicacao"},

        # RESEARCH
        {"ordem": 20, "texto": f"O que é GEO marketing", "categoria": "RESEARCH", "intent": "informacional", "persona": "estudante", "formato_esperado": "explicacao"},
    ]
