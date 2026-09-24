import re
from uuid import uuid4

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.adapters import get_adapter
from app.adapters.openfema.base import OpenFEMAUnavailable
from app.core.clock import today
from app.features.declarations.service import _date, _months_before, build_declarations
from app.features.programs.service import build_program_cards
from app.features.rules.service import rules_for_declaration

router = APIRouter()
FIPS_PATTERN = re.compile(r"[0-9]{5}")


def _error(request_id: str, status: int, code: str, message: str, retryable=False):
    return JSONResponse(
        status_code=status,
        content={
            "request_id": request_id,
            "error": {"code": code, "message": message, "retryable": retryable},
        },
    )


def _valid(body) -> bool:
    if not isinstance(body, dict):
        return False
    number = body.get("disaster_number")
    county_fips = body.get("county_fips")
    answers = body.get("answers")
    return (
        isinstance(number, int)
        and not isinstance(number, bool)
        and number > 0
        and isinstance(county_fips, str)
        and FIPS_PATTERN.fullmatch(county_fips) is not None
        and body.get("lang") in {"en", "es"}
        and isinstance(answers, dict)
        and answers.get("housing") in {"own", "rent"}
        and isinstance(answers.get("lost_work_or_self_employed"), bool)
        and isinstance(answers.get("on_snap"), bool)
        and isinstance(answers.get("household_size"), int)
        and not isinstance(answers.get("household_size"), bool)
        and answers["household_size"] > 0
    )


def _program_declaration(rows: list[dict], county_fips: str, disaster_number: int):
    declaration = next(
        (
            row
            for row in build_declarations(rows, county_fips)
            if row["disaster_number"] == disaster_number
        ),
        None,
    )
    if declaration is not None:
        return declaration

    as_of = today()
    active_since = _months_before(as_of, 18)
    state_fips, county_code = county_fips[:2], county_fips[2:]
    matching = []
    for row in rows:
        if (
            row.get("disasterNumber") != disaster_number
            or row.get("fipsStateCode") != state_fips
            or row.get("fipsCountyCode") not in {county_code, "000"}
            or row.get("disasterCloseoutDate") is not None
            or row.get("declarationType") not in {"DR", "EM"}
        ):
            continue
        declared = _date(row.get("declarationDate"))
        if declared is not None and declared >= active_since:
            matching.append((row, declared))
    if not matching:
        return None

    row, declared = min(
        matching, key=lambda item: item[0].get("fipsCountyCode") == "000"
    )
    deadline = _date(row.get("lastIAFilingDate"))
    return {
        "disaster_number": disaster_number,
        "individual_assistance": bool(
            row.get("ihProgramDeclared") or row.get("iaProgramDeclared")
        ),
        "registration_deadline": deadline.isoformat() if deadline else None,
        "registration_open": deadline is not None and as_of <= deadline,
        "rules_regime": rules_for_declaration(declared)["rules_regime"],
    }


@router.post("/programs")
async def programs(request: Request):
    request_id = str(uuid4())
    try:
        body = await request.json()
    except ValueError:
        body = None
    if not _valid(body):
        return _error(
            request_id, 400, "invalid_input", "Check your answers and try again."
        )

    county_fips = body["county_fips"]
    disaster_number = body["disaster_number"]
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

    declaration = _program_declaration(rows, county_fips, disaster_number)
    if declaration is None:
        return _error(
            request_id, 400, "invalid_input", "The disaster number was not found."
        )

    return {
        "request_id": request_id,
        "cards": build_program_cards(
            disaster_number, declaration, body["answers"], body["lang"]
        ),
    }
