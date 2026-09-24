import os

import pytest

from app.adapters import get_adapter

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(os.getenv("APP_MODE") != "live", reason="needs live Azure"),
]


def test_query_returns_fema_result():
    results = get_adapter("search", "live").search("appeal")
    assert any("fema.gov" in r["url"] for r in results)
