from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BillMetadata:
    """Metadata extracted from a bill."""

    bill_number: Optional[str] = None
    title: Optional[str] = None
    introduction_date: Optional[str] = None


@dataclass
class BillSection:
    """A bill section with optional nested subsections."""

    title: str
    text: str
    subsections: List[BillSection] = field(default_factory=list)


@dataclass
class BillDocument:
    """Structured representation of a bill."""

    metadata: BillMetadata
    sections: List[BillSection]
    amendments: List[BillSection] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
