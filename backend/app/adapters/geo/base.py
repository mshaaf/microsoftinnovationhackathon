import json
from functools import lru_cache
from pathlib import Path

SERVICE_NAME = "geo"
BUNDLE_PATH = Path(__file__).resolve().parents[4] / "data/geo/zip_county.json"


@lru_cache(maxsize=1)
def _bundle():
    return json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))


def lookup(zip_code: str):
    bundle = _bundle()
    rows = bundle.get(zip_code)
    if rows is None:
        return None
    states = bundle["_metadata"]["state_fips_to_abbreviation"]
    return [
        {
            "state": states[state_fips],
            "county_fips": state_fips + county_code,
            "name": name,
        }
        for state_fips, county_code, name, _share in rows
    ]
