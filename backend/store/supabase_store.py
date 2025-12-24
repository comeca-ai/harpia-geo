"""
🗄️ Store do Supabase para persistência de dados
"""

import json
from typing import Optional, List
from datetime import datetime
from supabase import create_client, Client
from chatkit.store import Store
from chatkit.types import (
    ThreadMetadata,
    MessageItem,
    FileMetadata
)


class SupabaseStore(Store):
    """
    Implementação do Store usando Supabase como backend.
    """

    def __init__(self, supabase_url: str, supabase_key: str):
        self.client: Client = create_client(supabase_url, supabase_key)

    # ==================== THREADS ====================

    async def create_thread(self, thread: ThreadMetadata) -> ThreadMetadata:
        """Cria uma nova thread."""
        data = {
            "id": thread.id,
            "title": thread.title or "Nova Análise",
            "metadata": json.dumps(thread.metadata or {}),
            "created_at": datetime.utcnow().isoformat()
        }

        result = self.client.table("threads").insert(data).execute()

        if result.data:
            return thread

        raise Exception("Erro ao criar thread")

    async def get_thread(self, thread_id: str) -> Optional[ThreadMetadata]:
        """Busca uma thread pelo ID."""
        result = self.client.table("threads").select("*").eq("id", thread_id).execute()

        if result.data and len(result.data) > 0:
            row = result.data[0]
            return ThreadMetadata(
                id=row["id"],
                title=row.get("title"),
                metadata=json.loads(row.get("metadata", "{}"))
            )

        return None

    async def update_thread(self, thread: ThreadMetadata) -> ThreadMetadata:
        """Atualiza uma thread."""
        data = {
            "title": thread.title,
            "metadata": json.dumps(thread.metadata or {}),
            "updated_at": datetime.utcnow().isoformat()
        }

        result = self.client.table("threads").update(data).eq("id", thread.id).execute()

        if result.data:
            return thread

        raise Exception("Erro ao atualizar thread")

    async def delete_thread(self, thread_id: str) -> None:
        """Deleta uma thread."""
        self.client.table("threads").delete().eq("id", thread_id).execute()

    async def list_threads(
        self,
        user_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[ThreadMetadata]:
        """Lista threads, opcionalmente filtradas por user_id."""
        query = self.client.table("threads").select("*")

        if user_id:
            query = query.eq("user_id", user_id)

        result = query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()

        threads = []
        for row in result.data or []:
            threads.append(ThreadMetadata(
                id=row["id"],
                title=row.get("title"),
                metadata=json.loads(row.get("metadata", "{}"))
            ))

        return threads

    # ==================== MESSAGES ====================

    async def add_message(self, thread_id: str, message: MessageItem) -> MessageItem:
        """Adiciona uma mensagem à thread."""
        data = {
            "id": message.id,
            "thread_id": thread_id,
            "role": message.role,
            "content": json.dumps(message.content) if isinstance(message.content, (dict, list)) else message.content,
            "metadata": json.dumps(getattr(message, "metadata", {}) or {}),
            "created_at": datetime.utcnow().isoformat()
        }

        result = self.client.table("messages").insert(data).execute()

        if result.data:
            return message

        raise Exception("Erro ao adicionar mensagem")

    async def get_messages(
        self,
        thread_id: str,
        limit: int = 100,
        before_id: Optional[str] = None
    ) -> List[MessageItem]:
        """Busca mensagens de uma thread."""
        query = self.client.table("messages").select("*").eq("thread_id", thread_id)

        if before_id:
            # Busca mensagens antes de um ID específico
            query = query.lt("created_at", before_id)

        result = query.order("created_at", desc=False).limit(limit).execute()

        messages = []
        for row in result.data or []:
            content = row.get("content", "")
            try:
                content = json.loads(content)
            except (json.JSONDecodeError, TypeError):
                pass

            messages.append(MessageItem(
                id=row["id"],
                role=row["role"],
                content=content
            ))

        return messages

    # ==================== FILES ====================

    async def save_file(self, file: FileMetadata, content: bytes) -> FileMetadata:
        """Salva um arquivo."""
        # Upload para Supabase Storage
        path = f"files/{file.id}/{file.name}"

        self.client.storage.from_("harpia-files").upload(
            path,
            content,
            file_options={"content-type": file.mime_type or "application/octet-stream"}
        )

        # Salva metadados
        data = {
            "id": file.id,
            "name": file.name,
            "mime_type": file.mime_type,
            "size": len(content),
            "path": path,
            "created_at": datetime.utcnow().isoformat()
        }

        self.client.table("files").insert(data).execute()

        return file

    async def get_file(self, file_id: str) -> Optional[bytes]:
        """Busca conteúdo de um arquivo."""
        result = self.client.table("files").select("path").eq("id", file_id).execute()

        if result.data and len(result.data) > 0:
            path = result.data[0]["path"]
            response = self.client.storage.from_("harpia-files").download(path)
            return response

        return None

    # ==================== ANÁLISES (custom) ====================

    async def save_analise(
        self,
        thread_id: str,
        empresa: str,
        site: str,
        dados: dict,
        prompts: list
    ) -> str:
        """Salva uma análise completa."""
        # Salva análise
        analise_data = {
            "thread_id": thread_id,
            "empresa": empresa,
            "site": site,
            "dados": json.dumps(dados),
            "status": "completed",
            "created_at": datetime.utcnow().isoformat()
        }

        result = self.client.table("analises").insert(analise_data).execute()
        analise_id = result.data[0]["id"]

        # Salva prompts
        for prompt in prompts:
            prompt_data = {
                "analise_id": analise_id,
                "ordem": prompt.get("ordem"),
                "texto": prompt.get("texto"),
                "categoria": prompt.get("categoria"),
                "intent": prompt.get("intent"),
                "persona": prompt.get("persona"),
                "formato_esperado": prompt.get("formato_esperado")
            }
            self.client.table("prompts").insert(prompt_data).execute()

        return analise_id

    async def get_analise(self, analise_id: str) -> Optional[dict]:
        """Busca uma análise pelo ID."""
        result = self.client.table("analises").select("*").eq("id", analise_id).execute()

        if result.data and len(result.data) > 0:
            analise = result.data[0]

            # Busca prompts
            prompts_result = self.client.table("prompts").select("*").eq("analise_id", analise_id).order("ordem").execute()

            return {
                "id": analise["id"],
                "empresa": analise["empresa"],
                "site": analise["site"],
                "dados": json.loads(analise.get("dados", "{}")),
                "status": analise["status"],
                "prompts": prompts_result.data or [],
                "created_at": analise["created_at"]
            }

        return None

    async def save_teste_visibilidade(
        self,
        analise_id: str,
        resultados: dict
    ) -> str:
        """Salva resultado de teste de visibilidade."""
        data = {
            "analise_id": analise_id,
            "score_geral": resultados.get("score_geral", 0),
            "resultados": json.dumps(resultados),
            "created_at": datetime.utcnow().isoformat()
        }

        result = self.client.table("testes_visibilidade").insert(data).execute()

        return result.data[0]["id"]
