import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker, SchemaError, ValidationError
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
LETTERS = ROOT / "fixtures" / "letters"
SCENARIOS = ROOT / "fixtures" / "scenarios"
SNAPSHOT = ROOT / "fixtures" / "openfema" / "declarations_snapshot.json"
SCHEMAS = ROOT / "contracts" / "schemas"
WATERMARK = "SAMPLE — NOT A REAL FEMA LETTER"
SCENARIO_IDS = {f"S{number:02}" for number in range(1, 16)}
LETTER_IDS = {f"L{number:02}" for number in range(1, 9)}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(name: str, value: dict[str, Any], path: Path) -> None:
    schema_path = SCHEMAS / f"{name}.json"
    if not schema_path.is_file():
        return
    schema = load_json(schema_path)
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value),
        key=lambda error: list(map(str, error.absolute_path)),
    )
    if errors:
        error = errors[0]
        location = "/".join(map(str, error.absolute_path)) or "$"
        raise ValueError(f"{path.relative_to(ROOT)} at {location}: {error.message}")


def require_contract_schemas() -> bool:
    paths = [SCHEMAS / "scenario.json", SCHEMAS / "letter-expected.json"]
    present = [path.is_file() for path in paths]
    require(not any(present) or all(present), "P0-03 fixture schemas are incomplete")
    for path in paths:
        if path.is_file():
            Draft202012Validator.check_schema(load_json(path))
    return all(present)


def require_date(value: Any, label: str) -> None:
    require(isinstance(value, str), f"{label} must be a YYYY-MM-DD string")
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{label} must be a YYYY-MM-DD string") from error


def validate_letters(strict: bool) -> set[str]:
    text_paths = sorted(LETTERS.glob("L*.txt"))
    ids = {path.stem for path in text_paths}
    require(ids == LETTER_IDS, f"expected L01-L08 text files; found {sorted(ids)}")
    expected_ids = {
        path.name.removesuffix(".expected.json")
        for path in LETTERS.glob("L*.expected.json")
    }
    image_ids = {path.stem for path in LETTERS.glob("L*.png")}
    require(expected_ids == LETTER_IDS, "expected sidecars must exist for L01-L08 only")
    require(image_ids == LETTER_IDS, "rendered PNGs must exist for L01-L08 only")

    for letter_id in sorted(LETTER_IDS):
        text_path = LETTERS / f"{letter_id}.txt"
        expected_path = LETTERS / f"{letter_id}.expected.json"
        image_path = LETTERS / f"{letter_id}.png"
        require(expected_path.is_file(), f"missing {expected_path.relative_to(ROOT)}")
        require(image_path.is_file(), f"missing {image_path.relative_to(ROOT)}")

        expected = load_json(expected_path)
        require(expected.get("id") == letter_id, f"{expected_path.name}: id mismatch")
        require(
            expected.get("decision_type")
            in {"approved", "not_approved", "needs_information", "unclear"},
            f"{expected_path.name}: invalid decision_type",
        )
        require(
            isinstance(expected.get("reasons"), list),
            f"{expected_path.name}: reasons must be a list",
        )
        require(
            type(expected.get("disaster_number")) is int,
            f"{expected_path.name}: disaster_number must be an integer",
        )
        require_date(expected.get("letter_date"), f"{expected_path.name}: letter_date")
        if "appeal_due" in expected:
            require_date(expected["appeal_due"], f"{expected_path.name}: appeal_due")
        if letter_id in LETTER_IDS - {"L07"}:
            require(
                expected["disaster_number"] == 4936,
                f"{expected_path.name}: expected DR-4936",
            )
        if letter_id == "L03":
            require(
                expected["letter_date"] == "2026-09-15"
                and expected.get("appeal_due") == "2026-11-14",
                "L03 must use the demo letter and appeal dates",
            )
        fake_pii = expected.get("fake_pii")
        require(
            isinstance(fake_pii, list)
            and fake_pii
            and all(isinstance(item, str) and item for item in fake_pii),
            f"{expected_path.name}: fake_pii must be a non-empty list of strings",
        )

        text = text_path.read_text(encoding="utf-8")
        require(WATERMARK in text, f"{text_path.name}: missing sample watermark")
        if letter_id in LETTER_IDS - {"L07"}:
            require(
                "FEMA-4936-DR-HI" in text, f"{text_path.name}: missing demo disaster"
            )
        require(
            all(item in text for item in fake_pii),
            f"{text_path.name}: fake_pii value missing from OCR text",
        )
        with Image.open(image_path) as image:
            require(
                image.format == "PNG" and image.width > 0 and image.height > 0,
                f"{image_path.name}: invalid PNG",
            )
            image.verify()
        if strict:
            validate_schema("letter-expected", expected, expected_path)
    return ids


def validate_scenarios(strict: bool, letter_ids: set[str]) -> int:
    paths = sorted(SCENARIOS.glob("S*.yaml"))
    ids = {path.stem for path in paths}
    require(ids == SCENARIO_IDS, f"expected S01-S15; found {sorted(ids)}")

    for path in paths:
        scenario = yaml.safe_load(path.read_text(encoding="utf-8"))
        require(isinstance(scenario, dict), f"{path.name}: expected a YAML object")
        require(scenario.get("id") == path.stem, f"{path.name}: id mismatch")
        require(
            all(
                key in scenario
                for key in ("persona", "lang", "zip", "answers", "letter", "expected")
            ),
            f"{path.name}: missing required field",
        )
        require(scenario["lang"] in {"en", "es"}, f"{path.name}: lang must be en or es")
        require(
            isinstance(scenario["zip"], str)
            and re.fullmatch(r"\d{5}", scenario["zip"]),
            f"{path.name}: zip must be five digits",
        )
        require(
            isinstance(scenario["answers"], dict),
            f"{path.name}: answers must be an object",
        )
        require(
            isinstance(scenario["expected"], dict),
            f"{path.name}: expected must be an object",
        )
        expected = scenario["expected"]
        if path.stem == "S07":
            require(
                expected.get("programs")
                == {
                    "fema_ihp": "open",
                    "irs_relief": "likely",
                    "dua": "check_now",
                    "dsnap": "check_now",
                    "sba_loan": "optional",
                },
                "S07 must keep the gig-worker program tiers",
            )
        if path.stem == "S12":
            require(
                scenario["zip"] == "39426"
                and expected.get("needs_confirmation") is True,
                "S12 must use the multi-county ZIP and ask for confirmation",
            )
        if path.stem == "S13":
            require(
                scenario["zip"] == "02134"
                and expected.get("individual_assistance") is False,
                "S13 must use the no-declaration ZIP",
            )
        if path.stem == "S14":
            require(
                expected.get("rules_regime") == "pre-2024-03-22"
                and expected.get("serious_needs_available") is False,
                "S14 must exercise the pre-2024 rules regime",
            )
        letter = scenario["letter"]
        require(
            letter is None or letter in letter_ids,
            f"{path.name}: unknown letter {letter}",
        )
        if strict:
            validate_schema("scenario", scenario, path)
    return len(paths)


def validate_snapshot() -> int:
    rows = load_json(SNAPSHOT).get("DisasterDeclarationsSummaries")
    require(
        isinstance(rows, list) and rows, "OpenFEMA snapshot has no declaration rows"
    )
    require(
        any(
            row.get("disasterNumber") == 4936
            and row.get("state") == "HI"
            and row.get("fipsCountyCode") == "001"
            for row in rows
        ),
        "OpenFEMA snapshot is missing DR-4936 for Hawaii County",
    )
    mississippi = {
        row.get("fipsCountyCode")
        for row in rows
        if row.get("disasterNumber") == 4930 and row.get("state") == "MS"
    }
    require(
        {"045", "047", "109", "131"} <= mississippi,
        "OpenFEMA snapshot is missing DR-4930 S12 counties",
    )
    require(
        any(
            row.get("disasterNumber") == 9998
            and row.get("state") == "XX"
            and row.get("fipsCountyCode") == "000"
            for row in rows
        ),
        "OpenFEMA snapshot is missing the synthetic statewide row",
    )
    require(
        any(
            date.fromisoformat(row["declarationDate"][:10]) < date(2024, 3, 22)
            for row in rows
            if row.get("disasterNumber") == 9999
        ),
        "OpenFEMA snapshot is missing the synthetic pre-2024 declaration",
    )
    return len(rows)


def main() -> int:
    try:
        strict = require_contract_schemas()
        letter_ids = validate_letters(strict)
        scenario_count = validate_scenarios(strict, letter_ids)
        row_count = validate_snapshot()
    except (OSError, ValueError, yaml.YAMLError, SchemaError, ValidationError) as error:
        print(f"Fixture validation failed: {error}", file=sys.stderr)
        return 1
    mode = (
        "contract schemas" if strict else "structural checks (P0-03 schemas not merged)"
    )
    print(
        f"Validated {scenario_count} scenarios, {len(letter_ids)} letters, and {row_count} OpenFEMA rows using {mode}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
