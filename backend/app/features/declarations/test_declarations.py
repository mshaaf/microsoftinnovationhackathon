import copy
import importlib
import json
from datetime import date
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator, FormatChecker

from app.adapters.openfema.mock import Adapter as MockOpenFEMA
from app.core.clock import use_today
from app.main import app

ROOT = Path(__file__).resolve().parents[4]
FIXTURE = json.loads(
    (ROOT / "fixtures/openfema/declarations_snapshot.json").read_text(encoding="utf-8")
)["DisasterDeclarationsSummaries"]
DECLARATIONS_SCHEMA = json.loads(
    (ROOT / "contracts/schemas/declarations.json").read_text(encoding="utf-8")
)
ERROR_SCHEMA = json.loads(
    (ROOT / "contracts/schemas/error.json").read_text(encoding="utf-8")
)
client = TestClient(app)


def service():
    return importlib.import_module("app.features.declarations.service")


def test_mock_adapter_reads_county_and_statewide_fixture_rows():
    adapter = MockOpenFEMA()

    rows = adapter.declarations_for_county("99", "001")
    other_county_rows = adapter.declarations_for_county("99", "099")

    assert {row["fipsCountyCode"] for row in rows} == {"001", "000"}
    assert [row["disasterNumber"] for row in other_county_rows] == [9998]


def test_declarations_route_returns_demo_disaster_and_matches_contract():
    with use_today(date(2026, 9, 23)):
        response = client.get("/api/declarations?state=HI&county_fips=15001&lang=en")

    assert response.status_code == 200
    body = response.json()
    assert body["county"] == {
        "state": "HI",
        "county_fips": "15001",
        "name": "Hawaii County",
    }
    assert [row["disaster_number"] for row in body["declarations"]] == [4936]
    assert body["declarations"][0]["individual_assistance"] is True
    assert body["declarations"][0]["registration_deadline"] == "2026-11-01"
    Draft202012Validator(DECLARATIONS_SCHEMA, format_checker=FormatChecker()).validate(
        body
    )


def test_county_without_active_declaration_returns_empty_list():
    response = client.get("/api/declarations?state=MA&county_fips=25025")

    assert response.status_code == 200
    assert response.json()["county"] == {
        "state": "MA",
        "county_fips": "25025",
        "name": "Suffolk County",
    }
    assert response.json()["declarations"] == []


def test_wrong_state_for_fips_is_invalid_input():
    response = client.get("/api/declarations?state=MA&county_fips=15001")

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_input"


def test_openfema_failure_is_retryable_dependency_error(monkeypatch):
    router = importlib.import_module("app.features.declarations.router")

    class FailingAdapter:
        def declarations_for_county(self, state_fips, county_code):
            raise router.OpenFEMAUnavailable

    monkeypatch.setattr(router, "get_adapter", lambda service_name: FailingAdapter())
    response = client.get("/api/declarations?state=HI&county_fips=15001")

    assert response.status_code == 503
    body = response.json()
    assert body["error"]["code"] == "dependency_unavailable"
    assert body["error"]["retryable"] is True
    Draft202012Validator(ERROR_SCHEMA).validate(body)


def test_deduplicates_fixture_designated_areas_by_disaster_number():
    demo_row = next(row for row in FIXTURE if row["disasterNumber"] == 4936)
    duplicate = copy.deepcopy(demo_row)
    duplicate["id"] = "duplicate-fixture-row"

    with use_today(date(2026, 9, 23)):
        declarations = service().build_declarations([demo_row, duplicate], "15001")

    assert len(declarations) == 1
    assert declarations[0]["disaster_number"] == 4936


def test_statewide_row_applies_to_each_county_in_its_state():
    statewide = next(row for row in FIXTURE if row["fipsCountyCode"] == "000")

    with use_today(date(2026, 9, 23)):
        first_county = service().build_declarations([statewide], "99001")
        second_county = service().build_declarations([statewide], "99099")

    assert [row["disaster_number"] for row in first_county] == [9998]
    assert [row["disaster_number"] for row in second_county] == [9998]


def test_ia_flag_uses_either_openfema_flag():
    row = copy.deepcopy(next(row for row in FIXTURE if row["disasterNumber"] == 4936))
    row["ihProgramDeclared"] = False
    row["iaProgramDeclared"] = True

    with use_today(date(2026, 9, 23)):
        declarations = service().build_declarations([row], "15001")

    assert declarations[0]["individual_assistance"] is True


@pytest.mark.parametrize(
    "changes",
    [
        {"declarationDate": "2025-03-22T00:00:00.000Z"},
        {"disasterCloseoutDate": "2026-09-22T00:00:00.000Z"},
        {"ihProgramDeclared": False, "iaProgramDeclared": False},
        {"declarationType": "FM"},
    ],
)
def test_active_filter_rejects_old_closed_non_ia_and_fire_rows(changes):
    row = copy.deepcopy(next(row for row in FIXTURE if row["disasterNumber"] == 4936))
    row.update(changes)

    with use_today(date(2026, 9, 23)):
        declarations = service().build_declarations([row], "15001")

    assert declarations == []


def test_active_cutoff_is_inclusive_at_eighteen_months():
    row = copy.deepcopy(next(row for row in FIXTURE if row["disasterNumber"] == 4936))
    row["declarationDate"] = "2025-03-23T00:00:00.000Z"

    with use_today(date(2026, 9, 23)):
        declarations = service().build_declarations([row], "15001")

    assert [item["disaster_number"] for item in declarations] == [4936]


@pytest.mark.parametrize(
    ("today", "open_now"),
    [(date(2026, 11, 1), True), (date(2026, 11, 2), False)],
)
def test_registration_open_uses_clock_and_includes_deadline_day(today, open_now):
    row = next(row for row in FIXTURE if row["disasterNumber"] == 4936)

    with use_today(today):
        declarations = service().build_declarations([row], "15001")

    assert declarations[0]["registration_deadline"] == "2026-11-01"
    assert declarations[0]["registration_open"] is open_now
