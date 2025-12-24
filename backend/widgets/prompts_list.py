"""
📋 Widgets de Lista de Prompts
"""

from chatkit.widgets import (
    Card,
    Text,
    Markdown,
    List,
    ListItem
)


def prompts_list_widget(prompts: list, categoria: str = None) -> Card:
    """
    Lista de prompts com opção de filtrar por categoria.
    """
    # Filtra por categoria se especificado
    if categoria:
        prompts_filtrados = [p for p in prompts if p.get("categoria") == categoria]
        titulo = f"📋 Prompts {categoria} ({len(prompts_filtrados)})"
    else:
        prompts_filtrados = prompts
        titulo = f"📋 20 Prompts GEO Gerados"

    # Agrupa por categoria
    categorias = {}
    for p in prompts_filtrados:
        cat = p.get("categoria", "OUTROS")
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(p)

    # Monta markdown
    md_content = f"## {titulo}\n\n"

    categoria_emojis = {
        "BRANDED": "🏷️",
        "UNBRANDED": "🔍",
        "PROBLEM": "😰",
        "COMPARISON": "⚖️",
        "PURCHASE": "💰",
        "RESEARCH": "📚"
    }

    for cat, cat_prompts in categorias.items():
        emoji = categoria_emojis.get(cat, "📝")
        md_content += f"### {emoji} {cat} ({len(cat_prompts)})\n\n"

        for p in cat_prompts:
            ordem = p.get("ordem", "")
            texto = p.get("texto", "")
            persona = p.get("persona", "")

            md_content += f"**{ordem}.** {texto}\n"
            if persona:
                md_content += f"   *Persona: {persona}*\n"
            md_content += "\n"

    return Card(
        children=[
            Markdown(md_content)
        ],
        confirm={
            "label": "📥 Baixar PDF",
            "action": "download_pdf"
        },
        cancel={
            "label": "🧪 Testar nas LLMs",
            "action": "testar_visibilidade"
        }
    )


def prompt_card_widget(prompt: dict) -> Card:
    """
    Card individual de um prompt.
    """
    categoria_emojis = {
        "BRANDED": "🏷️",
        "UNBRANDED": "🔍",
        "PROBLEM": "😰",
        "COMPARISON": "⚖️",
        "PURCHASE": "💰",
        "RESEARCH": "📚"
    }

    categoria = prompt.get("categoria", "OUTROS")
    emoji = categoria_emojis.get(categoria, "📝")

    md_content = f"""
### {emoji} {categoria}

**Prompt:**
> {prompt.get("texto", "")}

**Detalhes:**
- **Intent:** {prompt.get("intent", "informacional")}
- **Persona:** {prompt.get("persona", "usuário geral")}
- **Formato esperado:** {prompt.get("formato_esperado", "texto")}
"""

    return Card(
        children=[
            Markdown(md_content)
        ],
        confirm={
            "label": "📋 Copiar",
            "action": "copiar_prompt",
            "payload": {"texto": prompt.get("texto", "")}
        }
    )


def prompts_resumo_widget(prompts: list) -> Card:
    """
    Resumo dos prompts por categoria.
    """
    # Conta por categoria
    contagem = {}
    for p in prompts:
        cat = p.get("categoria", "OUTROS")
        contagem[cat] = contagem.get(cat, 0) + 1

    categoria_emojis = {
        "BRANDED": "🏷️",
        "UNBRANDED": "🔍",
        "PROBLEM": "😰",
        "COMPARISON": "⚖️",
        "PURCHASE": "💰",
        "RESEARCH": "📚"
    }

    # Monta tabela
    md_content = f"""
## 📊 Resumo dos Prompts

| Categoria | Quantidade | Descrição |
|-----------|------------|-----------|
"""

    descricoes = {
        "BRANDED": "Mencionam sua marca",
        "UNBRANDED": "Problema genérico do nicho",
        "PROBLEM": "Dor específica do cliente",
        "COMPARISON": "Comparativos",
        "PURCHASE": "Intenção de compra",
        "RESEARCH": "Pesquisa educacional"
    }

    for cat, qtd in contagem.items():
        emoji = categoria_emojis.get(cat, "📝")
        desc = descricoes.get(cat, "Outros")
        md_content += f"| {emoji} {cat} | {qtd} | {desc} |\n"

    md_content += f"\n**Total:** {len(prompts)} prompts"

    return Card(
        children=[
            Markdown(md_content)
        ],
        confirm={
            "label": "Ver Todos",
            "action": "ver_todos_prompts"
        },
        cancel={
            "label": "Testar Visibilidade",
            "action": "testar_visibilidade"
        }
    )
