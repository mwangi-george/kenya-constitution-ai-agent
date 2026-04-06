from __future__ import annotations

import asyncio
from pathlib import Path

from app.core.config import settings
from app.db.initializer import DatabaseInitializer
from app.db.session import session_manager
from app.services.indexing_service import ConstitutionIndexingService


async def main() -> None:
    """Index the constitution PDF into pgvector."""
    pdf_path = Path(__file__).parent.parent / "data/constitution.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(
            "Place THE CONSTITUTION OF KENYA, 2010 PDF at app/data/constitution.pdf before indexing."
        )

    await DatabaseInitializer.initialize()

    async with session_manager.create_session() as db:
        service = ConstitutionIndexingService.create(
            db=db,
            pdf_path=str(pdf_path),
            document_name="THE CONSTITUTION OF KENYA, 2010",
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        indexed_count = await service.index_document(
            document_name="THE CONSTITUTION OF KENYA, 2010"
        )
        print(f"Indexed {indexed_count} chunks successfully.")


if __name__ == "__main__":
    asyncio.run(main())
