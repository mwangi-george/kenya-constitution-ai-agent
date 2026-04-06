from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_chatbot_service, get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chatbot_service import ConstitutionChatbotService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def ask_question(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """Return a grounded constitution answer."""
    chatbot_service = get_chatbot_service(db)
    return await chatbot_service.ask(payload.question)


@router.post("/stream")
async def stream_question(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    """Stream a grounded constitution answer via SSE."""
    chatbot_service = get_chatbot_service(db)
    generator = chatbot_service.stream_answer(payload.question)
    return StreamingResponse(generator, media_type="text/event-stream")
