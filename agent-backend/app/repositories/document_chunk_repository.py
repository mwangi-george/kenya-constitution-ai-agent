from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DocumentChunk


class DocumentChunkRepository:
    """Handles database operations for document chunks."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def replace_document_chunks(self, document_name: str, chunks: list[DocumentChunk]) -> None:
        """Replace all stored chunks for one document."""
        await self.db.execute(
            delete(DocumentChunk).where(DocumentChunk.document_name == document_name)
        )
        self.db.add_all(chunks)
        await self.db.commit()

    async def search_similar(self, query_embedding: list[float], limit: int) -> list[DocumentChunk]:
        """Return the most similar stored chunks for a query embedding."""
        statement = (
            select(DocumentChunk)
            .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
            .limit(limit)
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())
