from __future__ import annotations

from openai import AsyncOpenAI

from app.core.config import settings


class OpenAIEmbeddingService:
    """Generates embeddings using the OpenAI embeddings API."""

    def __init__(self, api_key: str, model_name: str) -> None:
        self.client = AsyncOpenAI(api_key=api_key)
        self.model_name = model_name

    @classmethod
    def from_settings(cls) -> "OpenAIEmbeddingService":
        """Create an embedder from application settings."""
        return cls(
            api_key=settings.openai_api_key,
            model_name=settings.openai_embedding_model,
        )

    async def embed_text(self, text: str) -> list[float]:
        """Embed a single text string."""
        response = await self.client.embeddings.create(
            model=self.model_name,
            input=text,
        )
        return list(response.data[0].embedding)

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed many text strings in one request."""
        response = await self.client.embeddings.create(
            model=self.model_name,
            input=texts,
        )
        return [list(item.embedding) for item in response.data]
