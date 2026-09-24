import importlib

import httpx
import pytest

from app.adapters.openfema import live
from app.adapters.openfema.base import OpenFEMAUnavailable
from app.adapters.openfema.mock import Adapter as MockAdapter


def test_mock_adapter_finds_disaster_number_in_snapshot():
    row = MockAdapter().declaration_by_number(4936)

    assert row is not None
    assert row["disasterNumber"] == 4936
    assert row["declarationDate"].startswith("2026-09-01")


def test_mock_adapter_returns_none_for_unknown_disaster_number():
    assert MockAdapter().declaration_by_number(987654) is None


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


def test_live_disaster_lookup_filters_and_selects_only_required_fields():
    requests = []

    def respond(request):
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "DisasterDeclarationsSummaries": [
                    {"disasterNumber": 4936, "declarationDate": "2026-09-01"}
                ]
            },
        )

    live._DISASTER_CACHE.clear()
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        row = live.Adapter(client=client).declaration_by_number(4936)

    assert row == {"disasterNumber": 4936, "declarationDate": "2026-09-01"}
    params = requests[0].url.params
    assert params["$filter"] == "disasterNumber eq 4936"
    assert params["$select"] == "disasterNumber,declarationDate"
    assert params["$top"] == "1"


def test_live_disaster_lookup_returns_none_when_no_row_matches():
    live._DISASTER_CACHE.clear()
    with httpx.Client(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                json={
                    "DisasterDeclarationsSummaries": [
                        {"disasterNumber": 4936, "declarationDate": "2026-09-01"}
                    ]
                },
            )
        )
    ) as client:
        assert live.Adapter(client=client).declaration_by_number(987654) is None


def test_live_disaster_lookup_caches_for_one_hour(monkeypatch):
    requests = []

    def respond(request):
        requests.append(request)
        declaration_date = "2026-09-01" if len(requests) == 1 else "2026-09-02"
        return httpx.Response(
            200,
            json={
                "DisasterDeclarationsSummaries": [
                    {"disasterNumber": 4936, "declarationDate": declaration_date}
                ]
            },
        )

    now = [100.0]
    monkeypatch.setattr(live.time, "monotonic", lambda: now[0])
    live._DISASTER_CACHE.clear()
    with httpx.Client(transport=httpx.MockTransport(respond)) as client:
        adapter = live.Adapter(client=client)
        first = adapter.declaration_by_number(4936)
        now[0] = 3699.0
        cached = adapter.declaration_by_number(4936)
        now[0] = 3701.0
        refreshed = adapter.declaration_by_number(4936)

    assert first == cached
    assert refreshed["declarationDate"] == "2026-09-02"
    assert len(requests) == 2


def test_live_disaster_lookup_wraps_upstream_failure():
    live._DISASTER_CACHE.clear()
    with (
        httpx.Client(
            transport=httpx.MockTransport(lambda request: httpx.Response(503))
        ) as client,
        pytest.raises(OpenFEMAUnavailable),
    ):
        live.Adapter(client=client).declaration_by_number(4936)
