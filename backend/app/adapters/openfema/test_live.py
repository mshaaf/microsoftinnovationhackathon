import importlib

import httpx
import pytest

from app.adapters.openfema import live


def test_live_adapter_queries_selected_county_and_statewide_rows():
    requests = []

    def respond(request):
        requests.append(request)
        return httpx.Response(
            200,
            json={"DisasterDeclarationsSummaries": [{"disasterNumber": 4936}]},
        )

    live._CACHE.clear()
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        rows = live.Adapter(client=client).declarations_for_county("15", "001")

    assert rows == [{"disasterNumber": 4936}]
    params = requests[0].url.params
    assert params["$filter"] == (
        "fipsStateCode eq '15' and (fipsCountyCode eq '001' or fipsCountyCode eq '000')"
    )
    assert "lastIAFilingDate" in params["$select"]
    assert params["$top"] == "1000"


def test_live_adapter_caches_rows_for_one_hour(monkeypatch):
    requests = []

    def respond(request):
        requests.append(request)
        return httpx.Response(
            200, json={"DisasterDeclarationsSummaries": [{"disasterNumber": 4936}]}
        )

    now = [100.0]
    monkeypatch.setattr(live.time, "monotonic", lambda: now[0])
    live._CACHE.clear()
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        adapter = live.Adapter(client=client)
        adapter.declarations_for_county("15", "001")
        now[0] = 3699.0
        adapter.declarations_for_county("15", "001")
        now[0] = 3701.0
        adapter.declarations_for_county("15", "001")

    assert len(requests) == 2


def test_live_adapter_wraps_http_failures_as_dependency_errors():
    def fail(request):
        return httpx.Response(503)

    error_type = importlib.import_module(
        "app.adapters.openfema.base"
    ).OpenFEMAUnavailable
    live._CACHE.clear()
    with (
        httpx.Client(transport=httpx.MockTransport(fail)) as client,
        pytest.raises(error_type),
    ):
        live.Adapter(client=client).declarations_for_county("15", "001")
