"""
📊 Widgets de Resultado do Diagnóstico
"""

from chatkit.widgets import (
    Card,
    Text,
    Markdown,
    List,
    ListItem,
    Progress
)


def resultado_diagnostico_widget(
    empresa: str,
    dados: dict,
    total_prompts: int = 20
) -> Card:
    """
    Card com resultado do diagnóstico inicial.
    """
    servicos = dados.get("servicos", [])
    diferenciais = dados.get("diferenciais", [])
    nicho = dados.get("nicho", "não identificado")

    # Monta markdown do resultado
    md_content = f"""
### ✅ Diagnóstico Concluído

**Empresa:** {empresa}
**Site:** {dados.get('site', '')}
**Nicho:** {nicho}

**Descrição:**
{dados.get('descricao', 'Não foi possível extrair descrição.')}
"""

    if servicos:
        md_content += "\n**Serviços identificados:**\n"
        for s in servicos[:5]:
            md_content += f"- {s}\n"

    if diferenciais:
        md_content += "\n**Diferenciais:**\n"
        for d in diferenciais[:3]:
            md_content += f"- {d}\n"

    return Card(
        children=[
            Markdown(md_content),
            Text(f"📝 {total_prompts} prompts GEO foram gerados!")
        ],
        status="success",
        confirm={
            "label": "Ver Prompts",
            "action": "mostrar_prompts"
        },
        cancel={
            "label": "Testar Visibilidade",
            "action": "testar_visibilidade"
        }
    )


def score_visibilidade_widget(resultados: dict) -> Card:
    """
    Card com score de visibilidade nas LLMs.
    """
    score = resultados.get("score_geral", 0)
    emoji = resultados.get("emoji", "⚪")
    classificacao = resultados.get("classificacao", "desconhecido")
    mensagem = resultados.get("mensagem", "")

    # Cor baseada no score
    if score >= 80:
        cor = "green"
    elif score >= 50:
        cor = "yellow"
    elif score >= 20:
        cor = "orange"
    else:
        cor = "red"

    # Monta detalhes por LLM
    llm_details = ""
    for llm, dados in resultados.get("resultados_por_llm", {}).items():
        mencoes = dados.get("mencoes", 0)
        total = dados.get("total", 5)
        llm_score = dados.get("score", 0)
        llm_details += f"\n| {llm.upper()} | {mencoes}/{total} | {llm_score}% |"

    md_content = f"""
## {emoji} Score de Visibilidade: {score}%

**Classificação:** {classificacao.upper()}

{mensagem}

### Resultados por LLM

| LLM | Menções | Score |
|-----|---------|-------|{llm_details}

---

**O que significa:**
- Testamos seus prompts em cada LLM
- Verificamos se sua empresa foi mencionada
- Score = % de vezes que você apareceu
"""

    return Card(
        children=[
            Markdown(md_content)
        ],
        status="info" if score >= 50 else "warning",
        confirm={
            "label": "💡 Como Melhorar",
            "action": "dicas_melhoria"
        },
        cancel={
            "label": "Nova Análise",
            "action": "nova_analise"
        }
    )


def dicas_melhoria_widget(score: float) -> Card:
    """
    Card com dicas para melhorar visibilidade.
    """
    if score < 20:
        nivel = "crítico"
        dicas = [
            "Crie conteúdo otimizado para IA (artigos, FAQs)",
            "Publique em sites de autoridade (LinkedIn, Medium)",
            "Adicione schema markup ao seu site",
            "Gere menções em sites de terceiros",
            "Responda perguntas em fóruns do seu nicho"
        ]
    elif score < 50:
        nivel = "melhorável"
        dicas = [
            "Aumente a frequência de publicações",
            "Foque em palavras-chave long-tail",
            "Busque parcerias para co-marketing",
            "Otimize suas páginas principais para IA"
        ]
    else:
        nivel = "bom"
        dicas = [
            "Mantenha a consistência de publicações",
            "Monitore mudanças nas respostas das IAs",
            "Expanda para novos tópicos do seu nicho",
            "Considere criar conteúdo em vídeo/podcast"
        ]

    dicas_md = "\n".join([f"- {d}" for d in dicas])

    md_content = f"""
## 💡 Dicas para Melhorar

Seu nível atual: **{nivel.upper()}**

### Ações recomendadas:

{dicas_md}

---

**Próximo passo:** Implementar as dicas acima e rodar nova análise em 30 dias.

Quer acompanhamento profissional? Conheça nossos planos!
"""

    return Card(
        children=[
            Markdown(md_content)
        ],
        confirm={
            "label": "Ver Planos",
            "action": "ver_planos"
        },
        cancel={
            "label": "Entendi",
            "action": "fechar"
        }
    )


def planos_widget() -> Card:
    """
    Card com planos e preços.
    """
    md_content = """
## 📦 Planos Harpia

### 🥉 Starter - R$97/mês
- 5 análises por mês
- Dashboard básico
- Relatório mensal por email
- Suporte por email

### 🥈 Pro - R$297/mês
- 20 análises por mês
- Dashboard completo
- Monitoramento semanal
- Dicas personalizadas
- Suporte prioritário

### 🥇 Agency - R$797/mês
- Análises ilimitadas
- Multi-clientes
- API de integração
- White-label
- Gerente de conta dedicado

---

*Todos os planos incluem 7 dias de teste grátis!*
"""

    return Card(
        children=[
            Markdown(md_content)
        ],
        confirm={
            "label": "Quero o Pro!",
            "action": "contratar_pro"
        },
        cancel={
            "label": "Falar com vendas",
            "action": "contato_vendas"
        }
    )
