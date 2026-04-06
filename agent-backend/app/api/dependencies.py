from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import session_manager
from app.services.chatbot_service import ConstitutionChatbotService
from app.services.retriever import ConstitutionRetriever


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a managed asynchronous database session."""
    async with session_manager.create_session() as db:
        yield db


def get_chatbot_service(db: AsyncSession) -> ConstitutionChatbotService:
    """Build the chatbot service for one request."""
    retriever = ConstitutionRetriever.create(db=db)
    return ConstitutionChatbotService(retriever=retriever)
