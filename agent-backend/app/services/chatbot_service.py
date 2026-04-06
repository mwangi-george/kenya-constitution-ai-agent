from __future__ import annotations

import json
from collections.abc import AsyncGenerator

from app.ai.constitution_agent import (
    streaming_constitution_agent,
    structured_constitution_agent,
)
from app.ai.deps import AgentDependencies
from app.db.models import DocumentChunk
from app.schemas.chat import ChatResponse, CitationSchema
from app.services.retriever import ConstitutionRetriever


class ConstitutionChatbotService:
    """Coordinates retrieval and grounded answer generation."""

    def __init__(self, retriever: ConstitutionRetriever) -> None:
        self.retriever = retriever

    async def ask(self, question: str) -> ChatResponse:
        """Return a grounded answer with traceable citations."""
        retrieved_chunks = await self.retriever.retrieve(question)
        context_block = self._build_context_block(question=question, chunks=retrieved_chunks)
        deps = AgentDependencies(question=question, context_block=context_block)

        result = await structured_constitution_agent.run(question, deps=deps)
        cited_ids = set(result.output.cited_chunk_ids)

        citations = [
            self._to_citation_schema(chunk)
            for chunk in retrieved_chunks
            if not cited_ids or chunk.chunk_id in cited_ids
        ]

        return ChatResponse(answer=result.output.answer, citations=citations)

    async def stream_answer(self, question: str) -> AsyncGenerator[str, None]:
        """Stream a grounded answer as proper Server-Sent Events (SSE)."""

        retrieved_chunks = await self.retriever.retrieve(question)
        context_block = self._build_context_block(question=question, chunks=retrieved_chunks)
        deps = AgentDependencies(question=question, context_block=context_block)

        # Stream tokens
        async with streaming_constitution_agent.run_stream(question, deps=deps) as result:
            async for text in result.stream_text(delta=True):
                payload = {"content": text}

                yield (
                    f"event: token\n"
                    f"data: {json.dumps(payload)}\n\n"
                )

        # Final completion event (with citations)
        citations = [
            self._to_citation_schema(chunk).model_dump()
            for chunk in retrieved_chunks
        ]

        completion_payload = {"citations": citations}

        yield (
            f"event: complete\n"
            f"data: {json.dumps(completion_payload)}\n\n"
        )

    @staticmethod
    def _build_context_block(question: str, chunks: list[DocumentChunk]) -> str:
        """Format retrieved chunks into a prompt-friendly context block."""
        lines = [f"User question: {question}", "", "Context sources:"]

        for chunk in chunks:
            lines.extend(
                [
                    f"- chunk_id: {chunk.chunk_id}",
                    f"  article_label: {chunk.article_label or 'Unknown'}",
                    f"  page_number: {chunk.page_number or 'Unknown'}",
                    f"  content: {chunk.content}",
                    "",
                ]
            )

        return "\n".join(lines)

    @staticmethod
    def _to_citation_schema(chunk: DocumentChunk) -> CitationSchema:
        """Convert a database model into an API citation schema."""
        return CitationSchema(
            chunk_id=chunk.chunk_id,
            article_label=chunk.article_label,
            page_number=chunk.page_number,
            excerpt=chunk.content[:500],
        )
