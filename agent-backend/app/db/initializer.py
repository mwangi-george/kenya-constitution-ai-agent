from __future__ import annotations

from sqlalchemy import text

from app.db.models import Base
from app.db.session import session_manager


class DatabaseInitializer:
    """Initializes PostgreSQL extensions and application tables."""

    @classmethod
    async def initialize(cls) -> None:
        """Create pgvector extension and all database tables."""
        async with session_manager.engine.begin() as connection:
            await connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            await connection.run_sync(Base.metadata.create_all)
