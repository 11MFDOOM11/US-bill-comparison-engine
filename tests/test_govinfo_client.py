from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from govinfo_client import GovInfoAPIClient


class DummyResponse:
    def __init__(
        self,
        status_code: int,
        data: Dict[str, Any],
        headers: Dict[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self._data = data
        self.headers = headers or {}
        self.text = "H.R. 1\nAn Act\nSECTION 1\nTest"
        self.encoding = "utf-8"

    def json(self) -> Dict[str, Any]:
        return self._data


def test_list_collections():
    session = MagicMock()
    session.request.return_value = DummyResponse(200, {"collections": [{"code": "BILLS"}]})
    client = GovInfoAPIClient("test", session=session)
    cols = client.list_collections()
    assert cols[0]["code"] == "BILLS"
    session.request.assert_called_once()


def test_get_bill_document():
    session = MagicMock()
    session.request.return_value = DummyResponse(200, {})
    client = GovInfoAPIClient("test", session=session)
    doc = client.get_bill_document("pkg")
    assert doc.sections
    session.request.assert_called_once()
