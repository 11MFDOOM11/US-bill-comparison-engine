from __future__ import annotations

import re
from typing import List

try:
    from transformers import pipeline
except Exception:  # pragma: no cover - optional dependency
    pipeline = None

try:
    import textstat
except Exception:  # pragma: no cover - optional dependency
    textstat = None

from bill_preprocessor.models import BillDocument
from .models import SummaryResult


class BillSummarizer:
    """Generate summaries for bills at three detail levels."""

    def __init__(self, model_name: str = "t5-small") -> None:
        self.model_name = model_name
        self._pipeline = None
        if pipeline is not None:
            try:
                self._pipeline = pipeline("summarization", model=model_name)
            except Exception:  # pragma: no cover - model download failure
                self._pipeline = None

    @staticmethod
    def _basic_summary(text: str, sentences: int) -> str:
        """Return the first ``sentences`` sentences from ``text``."""
        splits = re.split(r"(?<=[.!?])\s+", text)
        return " ".join(splits[:sentences])

    def _transformers_summary(self, text: str, max_length: int) -> str:
        if self._pipeline is None:
            return self._basic_summary(text, 3)
        result = self._pipeline(text, max_length=max_length, min_length=5)
        return result[0]["summary_text"]

    @staticmethod
    def _extract_numbers(text: str) -> List[str]:
        pattern = r"\$?\d+(?:,\d+)*(?:\.\d+)?%?"
        return re.findall(pattern, text)

    @staticmethod
    def _identify_parties(text: str) -> List[str]:
        parties = []
        for term in ["citizen", "business", "agency", "government"]:
            if term in text.lower():
                parties.append(term)
        return parties

    def summarize(self, document: BillDocument) -> SummaryResult:
        """Return multi-level summaries with extra information."""
        text = "\n".join(section.text for section in document.sections)
        executive = self._transformers_summary(text, 40)
        standard = self._transformers_summary(text, 120)
        detailed = self._transformers_summary(text, 250)
        numbers = self._extract_numbers(text)
        parties = self._identify_parties(text)
        return SummaryResult(
            executive=executive,
            standard=standard,
            detailed=detailed,
            numbers=numbers,
            affected_parties=parties,
        )

    @staticmethod
    def readability(text: str) -> float:
        """Return the Flesch-Kincaid grade level or 0 if unavailable."""
        if textstat is None:
            return 0.0
        try:
            return textstat.flesch_kincaid_grade(text)
        except Exception:  # pragma: no cover - textstat errors
            return 0.0
