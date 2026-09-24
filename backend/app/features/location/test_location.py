import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator

from app.main import app

client = TestClient(app)
ROOT = Path(__file__).resolve().parents[4]
LOCATION_SCHEMA = json.loads(
    (ROOT / "contracts/schemas/location.json").read_text(encoding="utf-8")
)
ERROR_SCHEMA = json.loads(
    (ROOT / "contracts/schemas/error.json").read_text(encoding="utf-8")
)


@pytest.mark.parametrize(
    ("zip_code", "state", "county_fips", "name"),
    [
        ("96704", "HI", "15001", "Hawaii County"),
        ("39426", "MS", "28109", "Pearl River County"),
        ("39426", "MS", "28045", "Hancock County"),
        ("00601", "PR", "72001", "Adjuntas Municipio"),
        ("02134", "MA", "25025", "Suffolk County"),
    ],
)
def test_known_zip_counties(zip_code, state, county_fips, name):
    response = client.post("/api/location", json={"zip": zip_code})

    assert response.status_code == 200
    data = response.json()
    assert {"state": state, "county_fips": county_fips, "name": name} in data[
        "counties"
    ]
    if zip_code == "96704":
        assert data["counties"] == [
            {"state": "HI", "county_fips": "15001", "name": "Hawaii County"}
        ]
        assert data["needs_confirmation"] is False
    if zip_code == "39426":
        assert [county["county_fips"] for county in data["counties"]] == [
            "28109",
            "28045",
        ]
        assert data["needs_confirmation"] is True


def test_location_response_matches_contract():
    response = client.post("/api/location", json={"zip": "96704"})

    assert response.status_code == 200
    Draft202012Validator(LOCATION_SCHEMA).validate(response.json())


@pytest.mark.parametrize(
    ("zip_code", "status", "code"),
    [("00000", 404, "zip_not_found"), ("12x45", 400, "invalid_input")],
)
def test_location_errors_match_contract(zip_code, status, code):
    response = client.post("/api/location", json={"zip": zip_code})

    assert response.status_code == status
    data = response.json()
    assert data["error"]["code"] == code
    Draft202012Validator(ERROR_SCHEMA).validate(data)
