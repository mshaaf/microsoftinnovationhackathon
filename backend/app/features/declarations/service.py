import calendar
import json
from datetime import date
from functools import lru_cache

from app.adapters.geo.base import BUNDLE_PATH
from app.core.clock import today
from app.features.rules.service import rules_for_declaration


@lru_cache(maxsize=1)
def _county_names() -> dict[tuple[str, str], str]:
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    state_names = bundle["_metadata"]["state_fips_to_abbreviation"]
    names = {}
    for zip_code, areas in bundle.items():
        if zip_code == "_metadata":
            continue
        for state_fips, county_code, name, _share in areas:
            state = state_names.get(state_fips)
            if state:
                names.setdefault((state, state_fips + county_code), name)
    return names


def county_info(state: str, county_fips: str) -> dict | None:
    name = _county_names().get((state, county_fips))
    if name is None:
        return None
    return {"state": state, "county_fips": county_fips, "name": name}


def _months_before(value: date, months: int) -> date:
    month = value.month - months
    year = value.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def _date(value: object) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def build_declarations(rows: list[dict], county_fips: str) -> list[dict]:
    as_of = today()
    active_since = _months_before(as_of, 18)
    state_fips, county_code = county_fips[:2], county_fips[2:]

    # Prefer the specific county row when a statewide row repeats the disaster.
    matching = sorted(
        (
            row
            for row in rows
            if row.get("fipsStateCode") == state_fips
            and row.get("fipsCountyCode") in {county_code, "000"}
        ),
        key=lambda row: row.get("fipsCountyCode") == "000",
    )
    declarations = {}
    for row in matching:
        individual_assistance = bool(
            row.get("ihProgramDeclared") or row.get("iaProgramDeclared")
        )
        declared = _date(row.get("declarationDate"))
        # R10: active IA is DR/EM, within 18 months, and not closed out.
        if not individual_assistance or declared is None or declared < active_since:
            continue
        if row.get("disasterCloseoutDate") is not None:
            continue
        if row.get("declarationType") not in {"DR", "EM"}:
            continue

        deadline = _date(row.get("lastIAFilingDate"))
        # The frozen response schema needs a filing date to represent this row.
        if deadline is None:
            continue

        number = row["disasterNumber"]
        if number in declarations:
            declarations[number]["individual_assistance"] |= individual_assistance
            continue

        declarations[number] = {
            "disaster_number": number,
            "title": row.get("declarationTitle") or "FEMA disaster declaration",
            "incident_type": row.get("incidentType") or "",
            "declaration_date": declared.isoformat(),
            "individual_assistance": individual_assistance,
            "registration_deadline": deadline.isoformat(),
            "registration_open": as_of <= deadline,
            **rules_for_declaration(declared),
            "fema_url": f"https://www.fema.gov/disaster/{number}",
        }

    return list(declarations.values())
