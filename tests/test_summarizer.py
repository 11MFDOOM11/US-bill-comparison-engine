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

    print("\n=== Preprocessed Document ===")
    print(f"Bill Number: {doc.metadata.bill_number}")
    for i, section in enumerate(doc.sections):
        print(f"\nSection {i}:")
        print(f"Title: {section.title}")
        print(f"Content: {section.content if hasattr(section, 'content') else 'No content'}")

    summarizer = BillSummarizer()
    summary = summarizer.summarize(doc)
    print("\n=== Summary Details ===")
    print(f"Executive Summary: {summary.executive}")
    print(f"Affected Parties: {summary.affected_parties}")
    print(f"Numbers Found: {summary.numbers}")

    assert summary.executive
    assert "citizen" in summary.affected_parties
    assert "$5,000,000" in summary.numbers
