"""
📋 Widgets de Formulários
"""

from chatkit.widgets import (
    Card,
    Text,
    TextInput,
    Select,
    Markdown
)


def nova_analise_form() -> Card:
    """
    Formulário para iniciar nova análise GEO.
    """
    return Card(
        asForm=True,
        children=[
            Markdown("## 🦅 Nova Análise GEO"),
            Text("Preencha os dados da empresa para começar:"),
            TextInput(
                name="empresa",
                label="Nome da Empresa",
                placeholder="Ex: Datarisk, Nubank, iFood...",
                required=True
            ),
            TextInput(
                name="site",
                label="URL do Site",
                placeholder="Ex: datarisk.io",
                required=True
            ),
            Select(
                name="nicho",
                label="Nicho (opcional)",
                options=[
                    {"label": "Fintech", "value": "fintech"},
                    {"label": "E-commerce", "value": "ecommerce"},
                    {"label": "SaaS", "value": "saas"},
                    {"label": "Serviços", "value": "servicos"},
                    {"label": "Saúde", "value": "saude"},
                    {"label": "Educação", "value": "educacao"},
                    {"label": "Varejo", "value": "varejo"},
                    {"label": "Outro", "value": "outro"}
                ]
            )
        ],
        confirm={
            "label": "🔍 Analisar Empresa",
            "action": "iniciar_analise"
        }
    )


def testar_llm_form(prompts_disponiveis: int = 20) -> Card:
    """
    Formulário para configurar teste de visibilidade.
    """
    return Card(
        asForm=True,
        children=[
            Markdown("## 🧪 Testar Visibilidade"),
            Text(f"Você tem {prompts_disponiveis} prompts gerados."),
            Text("Selecione as LLMs para testar:"),
            Select(
                name="llms",
                label="LLMs",
                multiple=True,
                options=[
                    {"label": "ChatGPT (OpenAI)", "value": "chatgpt"},
                    {"label": "Gemini (Google)", "value": "gemini"},
                    {"label": "Perplexity", "value": "perplexity"},
                    {"label": "Claude (Anthropic)", "value": "claude"}
                ]
            ),
            Select(
                name="quantidade",
                label="Quantos prompts testar?",
                options=[
                    {"label": "5 prompts (rápido)", "value": "5"},
                    {"label": "10 prompts (recomendado)", "value": "10"},
                    {"label": "Todos (20 prompts)", "value": "20"}
                ]
            )
        ],
        confirm={
            "label": "🚀 Iniciar Teste",
            "action": "testar_visibilidade"
        },
        cancel={
            "label": "Cancelar",
            "action": "cancelar"
        }
    )


def contato_form() -> Card:
    """
    Formulário de contato para planos pagos.
    """
    return Card(
        asForm=True,
        children=[
            Markdown("## 📞 Fale com a gente"),
            Text("Interessado em monitoramento contínuo?"),
            TextInput(
                name="nome",
                label="Seu Nome",
                required=True
            ),
            TextInput(
                name="email",
                label="Email",
                placeholder="seu@email.com",
                required=True
            ),
            TextInput(
                name="telefone",
                label="WhatsApp (opcional)",
                placeholder="11 99999-9999"
            ),
            Select(
                name="plano",
                label="Plano de interesse",
                options=[
                    {"label": "Starter - R$97/mês", "value": "starter"},
                    {"label": "Pro - R$297/mês", "value": "pro"},
                    {"label": "Agency - R$797/mês", "value": "agency"},
                    {"label": "Quero entender melhor", "value": "duvida"}
                ]
            )
        ],
        confirm={
            "label": "Enviar",
            "action": "enviar_contato"
        }
    )
