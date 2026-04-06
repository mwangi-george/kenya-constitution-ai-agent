from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True)
class ChunkPayload:
    """Represents one chunk ready for embedding and storage."""

    chunk_id: str
    document_name: str
    chunk_index: int
    article_label: str | None
    page_number: int | None
    content: str


class ConstitutionTextChunker:
    """Splits constitution pages into overlapping text chunks."""

    def __init__(self, chunk_size: int, chunk_overlap: int) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_pages(
        self,
        document_name: str,
        pages: list[dict[str, str | int | None]],
    ) -> list[ChunkPayload]:
        """Chunk extracted pages while carrying simple article metadata."""
        chunks: list[ChunkPayload] = []
        chunk_index = 0

        for page in pages:
            page_text = str(page["text"] or "").strip()
            if not page_text:
                continue

            article_label = self._extract_article_label(page_text)
            start = 0

            while start < len(page_text):
                end = min(start + self.chunk_size, len(page_text))
                chunk_text = page_text[start:end].strip()
                if chunk_text:
                    chunk_index += 1
                    chunks.append(
                        ChunkPayload(
                            chunk_id=f"chunk-{chunk_index:04d}",
                            document_name=document_name,
                            chunk_index=chunk_index,
                            article_label=article_label,
                            page_number=int(page["page_number"]) if page["page_number"] else None,
                            content=chunk_text,
                        )
                    )

                if end >= len(page_text):
                    break

                start = max(end - self.chunk_overlap, 0)

        return chunks

    @staticmethod
    def _extract_article_label(text: str) -> str | None:
        """Try to infer an article heading from chunk text."""
        match = re.search(r"\bArticle\s+\d+[A-Za-z-]*\b", text, flags=re.IGNORECASE)
        if not match:
            return None
        return match.group(0).title()
