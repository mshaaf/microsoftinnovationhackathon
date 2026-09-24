import re
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.adapters import get_adapter
from app.adapters.openfema.base import OpenFEMAUnavailable
from app.features.declarations.service import build_declarations, county_info

router = APIRouter()
STATE_PATTERN = re.compile(r"[A-Z]{2}")
FIPS_PATTERN = re.compile(r"[0-9]{5}")


def _error(request_id: str, status: int, code: str, message: str, retryable=False):
    return JSONResponse(
        status_code=status,
        content={
            "request_id": request_id,
            "error": {"code": code, "message": message, "retryable": retryable},
        },
    )


@router.get("/declarations")
def declarations(state: str | None = None, county_fips: str | None = None):
    request_id = str(uuid4())
    if (
        state is None
        or county_fips is None
        or STATE_PATTERN.fullmatch(state) is None
        or FIPS_PATTERN.fullmatch(county_fips) is None
    ):
        return _error(
            request_id, 400, "invalid_input", "Enter a valid state and county FIPS."
        )

    county = county_info(state, county_fips)
    if county is None:
        return _error(
            request_id, 400, "invalid_input", "The state and county FIPS do not match."
        )

    try:
        rows = get_adapter("openfema").declarations_for_county(
            county_fips[:2], county_fips[2:]
        )
    except OpenFEMAUnavailable:
        return _error(
            request_id,
            503,
            "dependency_unavailable",
            "FEMA declaration data is temporarily unavailable. Try again.",
            retryable=True,
        )

    checked_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    return {
        "request_id": request_id,
        "county": county,
        "declarations": build_declarations(rows, county_fips),
        "checked_at": checked_at,
    }
