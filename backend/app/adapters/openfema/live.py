import time
from typing import Any

import httpx

from app.adapters.base import UnconfiguredLiveAdapter

from .base import SERVICE_NAME, OpenFEMAAdapter, OpenFEMAUnavailable

ENDPOINT = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"
FIELDS = (
    "disasterNumber,declarationType,declarationDate,declarationTitle,incidentType,"
    "ihProgramDeclared,iaProgramDeclared,lastIAFilingDate,disasterCloseoutDate,"
    "fipsStateCode,fipsCountyCode,designatedArea"
)
CACHE_TTL_SECONDS = 3600
_CACHE: dict[tuple[str, str], tuple[float, list[dict]]] = {}


class Adapter(UnconfiguredLiveAdapter, OpenFEMAAdapter):
    service_name = SERVICE_NAME

    def __init__(self, client: httpx.Client | None = None):
        self._client = client

    def declarations_for_county(self, state_fips: str, county_code: str) -> list[dict]:
        key = (state_fips, county_code)
        cached = _CACHE.get(key)
        if cached is not None and cached[0] > time.monotonic():
            return cached[1]

        params = {
            "$filter": (
                f"fipsStateCode eq '{state_fips}' and "
                f"(fipsCountyCode eq '{county_code}' or fipsCountyCode eq '000')"
            ),
            "$orderby": "declarationDate desc",
            "$top": "1000",
            "$select": FIELDS,
        }
        try:
            if self._client is None:
                with httpx.Client(timeout=10.0) as client:
                    response = client.get(ENDPOINT, params=params)
            else:
                response = self._client.get(ENDPOINT, params=params, timeout=10.0)
            response.raise_for_status()
            payload: Any = response.json()
        except (httpx.HTTPError, ValueError) as error:
            raise OpenFEMAUnavailable("OpenFEMA request failed") from error

        rows = (
            payload.get("DisasterDeclarationsSummaries")
            if isinstance(payload, dict)
            else None
        )
        if not isinstance(rows, list):
            raise OpenFEMAUnavailable(
                "OpenFEMA response did not contain declaration rows"
            )

        # ponytail: simultaneous misses may duplicate one GET; per-key locks if traffic grows.
        _CACHE[key] = (time.monotonic() + CACHE_TTL_SECONDS, rows)
        return rows
