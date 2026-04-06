from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models import DocumentChunk
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.services.embedding_service import OpenAIEmbeddingService


class ConstitutionRetriever:
    """Retrieves the most relevant constitution chunks for a question."""

    def __init__(
        self,
        embedder: OpenAIEmbeddingService,
        repository: DocumentChunkRepository,
        top_k: int,
    ) -> None:
        self.embedder = embedder
        self.repository = repository
        self.top_k = top_k

    @classmethod
    def create(cls, db: AsyncSession) -> "ConstitutionRetriever":
        """Factory method for a fully wired retriever."""
        return cls(
            embedder=OpenAIEmbeddingService.from_settings(),
            repository=DocumentChunkRepository(db=db),
            top_k=settings.retrieval_top_k,
        )

    async def retrieve(self, question: str) -> list[DocumentChunk]:
        """Embed a question and fetch the nearest constitution chunks."""
        query_embedding = await self.embedder.embed_text(question)
        return await self.repository.search_similar(query_embedding=query_embedding, limit=self.top_k)
