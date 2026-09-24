import json
from functools import lru_cache
from pathlib import Path

from app.adapters.base import MockAdapter

from .base import OpenFEMAAdapter

FIXTURE_PATH = (
    Path(__file__).resolve().parents[4] / "fixtures/openfema/declarations_snapshot.json"
)


@lru_cache(maxsize=1)
def _rows() -> list[dict]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return fixture["DisasterDeclarationsSummaries"]


class Adapter(MockAdapter, OpenFEMAAdapter):
    def declarations_for_county(self, state_fips: str, county_code: str) -> list[dict]:
        return [
            row
            for row in _rows()
            if row["fipsStateCode"] == state_fips
            and row["fipsCountyCode"] in {county_code, "000"}
        ]

    def declaration_by_number(self, disaster_number: int) -> dict | None:
        return next(
            (row for row in _rows() if row["disasterNumber"] == disaster_number), None
        )
