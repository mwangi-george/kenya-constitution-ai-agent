from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


class PDFConstitutionLoader:
    """Loads text and page metadata from a PDF constitution document."""

    def __init__(self, pdf_path: str | Path) -> None:
        self.pdf_path = Path(pdf_path)

    def load_pages(self) -> list[dict[str, str | int | None]]:
        """Return extracted text grouped by PDF page."""
        reader = PdfReader(str(self.pdf_path))
        pages: list[dict[str, str | int | None]] = []

        for index, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append(
                {
                    "page_number": index,
                    "text": self._normalize_text(text),
                }
            )

        return pages

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Collapse excessive whitespace for cleaner indexing."""
        return " ".join(text.split())
