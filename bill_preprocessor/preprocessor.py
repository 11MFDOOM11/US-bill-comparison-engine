from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional

try:
    import spacy
except ImportError:  # pragma: no cover - spaCy may be unavailable in test env
    spacy = None

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - BeautifulSoup may be unavailable
    BeautifulSoup = None  # type: ignore

try:
    from pdfminer.high_level import extract_text as pdf_extract_text
except ImportError:  # pragma: no cover - pdfminer may be unavailable
    pdf_extract_text = None  # type: ignore

if spacy is not None:
    from spacy.language import Language
else:  # pragma: no cover - spaCy not installed
    Language = object  # type: ignore

from .models import BillDocument, BillMetadata, BillSection


class BillPreprocessor:
    """Preprocess and structure bill text."""

    HEADER_PATTERN = re.compile(r"^\s*(?:Page\s+\d+|\w+\s+Congress)\s*$", re.IGNORECASE)
    SECTION_PATTERN = re.compile(r"^(section\s+\d+|sec\.\s*\d+)", re.IGNORECASE)
    AMENDMENT_PATTERN = re.compile(r"^amendments?", re.IGNORECASE)
    REFERENCES_PATTERN = re.compile(r"^references?", re.IGNORECASE)

    def __init__(self, nlp: Optional[Language] = None) -> None:
        if nlp is None:
            if spacy is None:
                self.nlp = None
                return
            try:
                nlp = spacy.load("en_core_web_sm")
            except Exception:
                nlp = spacy.blank("en")
        self.nlp = nlp

    def load_text(self, path: str) -> str:
        """Return text content depending on file type."""
        ext = Path(path).suffix.lower()
        if ext == ".pdf":
            return self._extract_text_from_pdf(path)
        text = Path(path).read_text(encoding="utf-8")
        if ext in {".html", ".htm"}:
            return self._extract_text_from_html(text)
        return text

    @staticmethod
    def _extract_text_from_pdf(path: str) -> str:
        if pdf_extract_text is None:
            raise ImportError("pdfminer.six is required to read PDF files")
        try:
            return pdf_extract_text(path)
        except Exception as exc:
            raise ValueError(f"Could not read PDF: {path}") from exc

    @staticmethod
    def _extract_text_from_html(html: str) -> str:
        if BeautifulSoup is None:
            raise ImportError("BeautifulSoup is required to parse HTML")
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n")

    def preprocess(self, text: str) -> BillDocument:
        """Clean raw text and return a structured bill document."""
        lines = [line for line in text.splitlines() if line.strip()]
        cleaned_lines = [ln for ln in lines if not self.HEADER_PATTERN.match(ln)]
        cleaned_text = "\n".join(cleaned_lines)

        metadata = self._extract_metadata(cleaned_text)
        sections = self._split_sections(cleaned_lines)
        amendments = [s for s in sections if self.AMENDMENT_PATTERN.match(s.title)]
        references = [s.text for s in sections if self.REFERENCES_PATTERN.match(s.title)]
        main_sections = [s for s in sections if s not in amendments]

        return BillDocument(
            metadata=metadata,
            sections=main_sections,
            amendments=amendments,
            references=references,
        )

    def _extract_metadata(self, text: str) -> BillMetadata:
        bill_number_match = re.search(r"(H\.R\.|S\.)\s*\d+", text)
        title_match = re.search(r"^An?\s+Act\s+.*", text, re.MULTILINE)
        date_match = re.search(
            r"introduced\s+(?:on\s+)?([A-Za-z]+\s+\d{1,2},\s+\d{4})",
            text,
            re.IGNORECASE,
        )
        return BillMetadata(
            bill_number=bill_number_match.group(0) if bill_number_match else None,
            title=title_match.group(0) if title_match else None,
            introduction_date=date_match.group(1) if date_match else None,
        )

    def _split_sections(self, lines: List[str]) -> List[BillSection]:
        sections: List[BillSection] = []
        current_title = "Intro"
        current_text: List[str] = []
        for line in lines:
            if self.SECTION_PATTERN.match(line):
                if current_text:
                    sections.append(
                        BillSection(title=current_title, text="\n".join(current_text))
                    )
                current_title = line.strip()
                current_text = []
                continue
            current_text.append(line)
        if current_text:
            sections.append(
                BillSection(title=current_title, text="\n".join(current_text))
            )
        return sections
