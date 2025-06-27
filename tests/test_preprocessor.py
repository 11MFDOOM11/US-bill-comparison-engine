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
    assert doc.metadata.bill_number == "H.R. 1234"
    assert len(doc.sections) == 3
    assert doc.sections[1].title.lower().startswith("section 1")

    cleaned = preprocessor.prepare_document(doc)
    assert "page 1" not in cleaned
    assert "SECTION 1" in cleaned

