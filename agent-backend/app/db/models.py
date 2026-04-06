from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.core.config import settings


class Base(DeclarativeBase):
    """Declarative base for SQLAlchemy models."""


class DocumentChunk(Base):
    """Stores a searchable chunk of the constitution and its embedding."""

    __tablename__ = "document_chunks"

    chunk_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    document_name: Mapped[str] = mapped_column(String(255), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, index=True)
    article_label: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(settings.embedding_dimensions), nullable=False)
