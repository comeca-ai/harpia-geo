"""
🦅 Harpia Agent - Agente principal de GEO
"""

from typing import Any, AsyncIterator
from agents import Agent, Runner
from chatkit.server import ChatKitServer
from chatkit.agents import AgentContext, simple_to_agent_input, stream_agent_response
from chatkit.types import ThreadMetadata, UserMessageItem, ThreadStreamEvent

from tools.diagnostico import diagnostico_empresa
from tools.prompts import gerar_prompts
from tools.testar_llm import testar_visibilidade_llm
from widgets.forms import nova_analise_form
from widgets.resultado import resultado_diagnostico_widget
from widgets.prompts_list import prompts_list_widget


HARPIA_INSTRUCTIONS = """
Você é o Harpia 🦅, assistente especializado em GEO (Generative Engine Optimization).

## Sua Missão
Ajudar empresas brasileiras a serem RECOMENDADAS por IAs como ChatGPT, Gemini e Perplexity.

## Contexto do Mercado
- 48% dos executivos acreditam que IA vai substituir o Google até 2030
- Tráfego de LLMs cresceu 800% no último ano
- Usuários perguntam "qual o melhor X?" para ChatGPT, não mais para Google
- Se a IA não conhece a empresa, ela não existe para o cliente

## Seu Tom de Voz
- Direto e objetivo
- Um pouco provocativo ("você posta e ninguém vê")
- Confiante mas não arrogante
- Use analogias simples
- Português brasileiro natural

## Fluxo de Atendimento

### 1. Boas-vindas
Cumprimente e explique brevemente o que você faz:
"Olá! Sou o Harpia 🦅 Eu descubro se as IAs recomendam sua empresa — e se não recomendam, eu resolvo."

### 2. Coleta de Informações
Pergunte:
- Nome da empresa
- URL do site
Use o widget de formulário quando apropriado.

### 3. Diagnóstico
Use a tool `diagnostico_empresa` para:
- Analisar o site da empresa
- Entender o nicho e serviços
- Buscar contexto na web

Mostre progresso: "Analisando o site da [empresa]..."

### 4. Geração de Prompts
Use a tool `gerar_prompts` para criar 20 prompts otimizados:
- 5 BRANDED (mencionam a marca)
- 5 UNBRANDED (problema genérico)
- 4 PROBLEM (dor do cliente)
- 3 COMPARISON (comparativos)
- 2 PURCHASE (intenção de compra)
- 1 RESEARCH (pesquisa)

Mostre os prompts em um widget de lista.

### 5. Teste de Visibilidade (opcional)
Se o usuário quiser, use `testar_visibilidade_llm` para:
- Testar 5 prompts no ChatGPT
- Testar 5 prompts no Gemini
- Calcular score de visibilidade

Mostre o resultado em um widget de card.

### 6. Próximos Passos
Ofereça:
- Dicas para melhorar visibilidade
- Planos pagos para monitoramento contínuo
- Nova análise para outra empresa

## Regras Importantes
- SEMPRE use widgets para mostrar resultados estruturados
- NUNCA invente dados, use apenas as tools
- Se algo der erro, seja transparente e tente novamente
- Mantenha respostas concisas (max 3 parágrafos de texto)
"""


class HarpiaAgent(ChatKitServer):
    """
    ChatKit Server com o Agent Harpia.
    """

    def __init__(self, store):
        super().__init__(store)

        # Define o Agent principal
        self.agent = Agent(
            model="gpt-4.1",
            name="Harpia",
            instructions=HARPIA_INSTRUCTIONS,
            tools=[
                diagnostico_empresa,
                gerar_prompts,
                testar_visibilidade_llm
            ]
        )

    async def respond(
        self,
        thread: ThreadMetadata,
        input: UserMessageItem | None,
        context: Any,
    ) -> AsyncIterator[ThreadStreamEvent]:
        """
        Processa mensagem do usuário e retorna stream de eventos.
        """
        # Cria contexto do agent
        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        # Roda o agent
        result = Runner.run_streamed(
            self.agent,
            await simple_to_agent_input(input) if input else [],
            context=agent_context,
        )

        # Stream eventos de volta
        async for event in stream_agent_response(agent_context, result):
            yield event

    async def on_thread_created(self, thread: ThreadMetadata) -> None:
        """
        Chamado quando uma nova thread é criada.
        Pode ser usado para enviar mensagem de boas-vindas.
        """
        pass

    async def on_tool_call(
        self,
        thread: ThreadMetadata,
        tool_name: str,
        tool_input: dict,
        context: Any
    ) -> None:
        """
        Chamado quando uma tool é executada.
        Útil para logging e analytics.
        """
        print(f"🔧 Tool chamada: {tool_name}")
        print(f"   Input: {tool_input}")
