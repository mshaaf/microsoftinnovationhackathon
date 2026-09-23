import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, SchemaError, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "contracts" / "schemas"
EXAMPLES = ROOT / "contracts" / "examples"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_payload(schema: dict, payload: dict) -> None:
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(payload)


def test_rejects_mismatched_declaration_example() -> None:
    schema = load_json(SCHEMAS / "declarations.json")
    payload = load_json(EXAMPLES / "declarations.json")
    payload["declarations"][0]["registration_open"] = "true"
    try:
        validate_payload(schema, payload)
    except ValidationError:
        return
    raise AssertionError("validator accepted a string for registration_open")


def validate_examples() -> int:
    schemas = {path.stem: path for path in SCHEMAS.glob("*.json")}
    examples = {path.stem: path for path in EXAMPLES.glob("*.json")}
    if schemas.keys() != examples.keys():
        missing = sorted(schemas.keys() - examples.keys())
        unknown = sorted(examples.keys() - schemas.keys())
        raise ValueError(f"missing examples: {missing}; missing schemas: {unknown}")

    for name, schema_path in sorted(schemas.items()):
        schema = load_json(schema_path)
        Draft202012Validator.check_schema(schema)
        example_path = examples[name]
        try:
            validate_payload(schema, load_json(example_path))
        except ValidationError as error:
            location = "/".join(map(str, error.absolute_path)) or "$"
            raise ValueError(
                f"{example_path.relative_to(ROOT)} at {location}: {error.message}"
            ) from error
    return len(examples)


def main() -> int:
    try:
        test_rejects_mismatched_declaration_example()
        count = validate_examples()
    except (OSError, ValueError, SchemaError, ValidationError) as error:
        print(f"Contract validation failed: {error}", file=sys.stderr)
        return 1
    print("Validator mismatch check passed.")
    print(f"Validated {count} contract examples against their schemas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
