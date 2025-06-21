from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from bill_preprocessor import BillPreprocessor

SAMPLE_TEXT = """\
H.R. 1234
An Act To Improve Something

SECTION 1
This is the first section.

SECTION 2
This is the second section.
page 1
"""


def test_preprocess_basic():
    preprocessor = BillPreprocessor()
    doc = preprocessor.preprocess(SAMPLE_TEXT)

    # Print the full document structure
    print("\n=== Full Document Structure ===")
    print(f"Bill Number: {doc.metadata.bill_number}")
    print("\nAll Sections:")
    for i, section in enumerate(doc.sections):
        print(f"\nSection {i}:")
        print(f"Title: {section.title}")
        print(f"Content: {section.content if hasattr(section, 'content') else 'No content'}")

    assert doc.metadata.bill_number == "H.R. 1234"
    print(f"\nFound {len(doc.sections)} sections")

    assert len(doc.sections) == 3
    assert doc.sections[1].title.lower().startswith("section 1")

