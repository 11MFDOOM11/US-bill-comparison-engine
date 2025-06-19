from __future__ import annotations

from dataclasses import dataclass
from typing import List

@dataclass
class SummaryResult:
    """Holds bill summaries for different detail levels."""

    executive: str
    standard: str
    detailed: str
    numbers: List[str]
    affected_parties: List[str]
