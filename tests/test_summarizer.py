from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from bill_preprocessor import BillPreprocessor
from bill_summarizer import BillSummarizer

SAMPLE_TEXT = """\
H.R. 1234
An Act To Improve Something

SECTION 1
This act allocates $5,000,000 for infrastructure improvements.
Citizens shall benefit from the new funding.

SECTION 2
Businesses must comply with new regulations.
"""


def test_summarize_basic():
    preprocessor = BillPreprocessor()
    doc = preprocessor.preprocess(SAMPLE_TEXT)
    summarizer = BillSummarizer()
    summary = summarizer.summarize(doc)
    assert summary.executive
    assert "citizen" in summary.affected_parties
    assert "$5,000,000" in summary.numbers
