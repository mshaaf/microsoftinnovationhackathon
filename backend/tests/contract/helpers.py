import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SCHEMAS = Path(__file__).resolve().parents[3] / "contracts" / "schemas"


def assert_matches_schema(response: Any, name: str) -> None:
    schema = json.loads((SCHEMAS / f"{name}.json").read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(
            response.json()
        ),
        key=lambda error: list(map(str, error.absolute_path)),
    )
    if errors:
        details = "\n".join(
            f"{'/'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
            for error in errors
        )
        raise AssertionError(f"response does not match {name} schema:\n{details}")
