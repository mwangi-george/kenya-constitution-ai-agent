from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DocumentChunk
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.services.embedding_service import OpenAIEmbeddingService
from app.services.pdf_loader import PDFConstitutionLoader
from app.services.text_chunker import ConstitutionTextChunker


class ConstitutionIndexingService:
    """Builds the searchable vector index for the constitution PDF."""

    def __init__(
        self,
        loader: PDFConstitutionLoader,
        chunker: ConstitutionTextChunker,
        embedder: OpenAIEmbeddingService,
        repository: DocumentChunkRepository,
    ) -> None:
        self.loader = loader
        self.chunker = chunker
        self.embedder = embedder
        self.repository = repository

    async def index_document(self, document_name: str) -> int:
        """Load, chunk, embed, and store the constitution document."""
        pages = self.loader.load_pages()
        chunk_payloads = self.chunker.chunk_pages(document_name=document_name, pages=pages)
        embeddings = await self.embedder.embed_texts([chunk.content for chunk in chunk_payloads])

        models = [
            DocumentChunk(
                chunk_id=chunk.chunk_id,
                document_name=chunk.document_name,
                chunk_index=chunk.chunk_index,
                article_label=chunk.article_label,
                page_number=chunk.page_number,
                content=chunk.content,
                embedding=embedding,
            )
            for chunk, embedding in zip(chunk_payloads, embeddings, strict=True)
        ]

        await self.repository.replace_document_chunks(document_name=document_name, chunks=models)
        return len(models)

    @classmethod
    def create(
        cls,
        db: AsyncSession,
        pdf_path: str,
        document_name: str,
        chunk_size: int,
        chunk_overlap: int,
    ) -> "ConstitutionIndexingService":
        """Factory method for a fully wired indexing service."""
        return cls(
            loader=PDFConstitutionLoader(pdf_path=pdf_path),
            chunker=ConstitutionTextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap),
            embedder=OpenAIEmbeddingService.from_settings(),
            repository=DocumentChunkRepository(db=db),
        )
