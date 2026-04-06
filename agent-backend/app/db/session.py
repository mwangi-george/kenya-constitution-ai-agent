from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


class DatabaseSessionManager:
    """Creates and manages async database sessions."""

    def __init__(self, database_url: str) -> None:
        self.engine = create_async_engine(database_url, echo=False, future=True)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    def create_session(self) -> AsyncSession:
        """Create a new asynchronous database session."""
        return self.session_factory()


session_manager = DatabaseSessionManager(settings.async_db_url)
