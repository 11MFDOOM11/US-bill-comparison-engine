from __future__ import annotations

import logging
import time
from functools import lru_cache
from typing import Any, Dict, List, Optional

try:
    import requests
except Exception:  # pragma: no cover - optional dependency
    requests = None  # type: ignore

from bill_preprocessor.preprocessor import BillPreprocessor
from bill_preprocessor.models import BillDocument

logger = logging.getLogger(__name__)


class GovInfoAPIError(Exception):
    """Raised when the GovInfo API returns an error."""


class GovInfoAPIClient:
    """Client for the GovInfo API with basic caching and retry logic."""

    BASE_URL = "https://api.govinfo.gov"

    def __init__(self, api_key: str, session: Optional[Any] = None) -> None:
        if requests is None and session is None:
            raise ImportError("requests is required to use GovInfoAPIClient")
        self.api_key = api_key
        self.session = session or requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> Any:
        url = f"{self.BASE_URL}{endpoint}"
        params = kwargs.pop("params", {})
        params["api_key"] = self.api_key
        backoff = 1
        while True:
            response = self.session.request(method, url, params=params, **kwargs)
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", backoff))
                logger.warning("Rate limited, sleeping for %s seconds", retry_after)
                time.sleep(retry_after)
                backoff = min(backoff * 2, 60)
                continue
            if response.status_code == 503:
                retry_after = int(response.headers.get("Retry-After", backoff))
                logger.warning("Service unavailable, retrying in %s seconds", retry_after)
                time.sleep(retry_after)
                backoff = min(backoff * 2, 60)
                continue
            if 400 <= response.status_code:
                raise GovInfoAPIError(
                    f"API error {response.status_code}: {response.text}"
                )
            return response

    @lru_cache(maxsize=128)
    def list_collections(self) -> List[Dict[str, Any]]:
        """Return available collections."""
        resp = self._request("GET", "/collections")
        return resp.json().get("collections", [])

    @lru_cache(maxsize=128)
    def get_package_summary(self, package_id: str) -> Dict[str, Any]:
        """Return metadata for a package."""
        resp = self._request("GET", f"/packages/{package_id}/summary")
        return resp.json()

    @lru_cache(maxsize=128)
    def get_bill_text(self, package_id: str) -> str:
        """Return raw XML text for a bill package."""
        resp = self._request("GET", f"/packages/{package_id}/xml")
        resp.encoding = "utf-8"
        return resp.text

    def search_bills(
        self,
        query: str,
        congress: Optional[int] = None,
        last_modified: Optional[str] = None,
        page: int = 1,
        page_size: int = 25,
    ) -> List[Dict[str, Any]]:
        """Search for bills using the GovInfo search service."""
        payload: Dict[str, Any] = {"query": query, "offset": (page - 1) * page_size, "pageSize": page_size}
        if congress:
            payload["congress"] = congress
        if last_modified:
            payload["lastModified"] = last_modified
        resp = self._request("POST", "/search", json=payload)
        data = resp.json()
        return data.get("results", [])

    def get_bill_document(self, package_id: str) -> BillDocument:
        """Return a ``BillDocument`` for the given package."""
        xml_text = self.get_bill_text(package_id)
        preprocessor = BillPreprocessor()
        doc = preprocessor.preprocess(xml_text)
        return doc
