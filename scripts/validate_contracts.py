import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, SchemaError, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "contracts" / "schemas"
EXAMPLES = ROOT / "contracts" / "examples"
REQUIRED_CONTRACTS = frozenset(
    {
        "chat",
        "checklist",
        "declarations",
        "error",
        "escalate",
        "health",
        "ihp_rules",
        "letter-decode",
        "letter-expected",
        "location",
        "programs",
        "programs_data",
        "reason_taxonomy",
        "scenario",
    }
)


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


def require_complete_contract_set(
    schema_names: set[str], example_names: set[str]
) -> None:
    if schema_names != example_names:
        raise ValueError("schema and example names do not match")
    missing = sorted(REQUIRED_CONTRACTS - schema_names)
    unknown = sorted(schema_names - REQUIRED_CONTRACTS)
    if missing or unknown:
        raise ValueError(
            f"missing required contracts: {missing}; unknown contracts: {unknown}"
        )


def test_rejects_missing_contract_pair() -> None:
    incomplete = set(REQUIRED_CONTRACTS - {"programs_data"})
    try:
        require_complete_contract_set(incomplete, incomplete)
    except ValueError:
        return
    raise AssertionError("validator accepted a missing schema/example pair")


def test_rejects_unknown_rule_regime() -> None:
    for name in ("declarations", "checklist"):
        schema = load_json(SCHEMAS / f"{name}.json")
        payload = load_json(EXAMPLES / f"{name}.json")
        if name == "declarations":
            payload["declarations"][0]["rules_regime"] = "2024-03-23"
        else:
            payload["rules_regime"] = "2024-03-23"
        try:
            validate_payload(schema, payload)
        except ValidationError:
            continue
        raise AssertionError(f"validator accepted an unknown {name} rules_regime")


def validate_examples() -> int:
    schemas = {path.stem: path for path in SCHEMAS.glob("*.json")}
    examples = {path.stem: path for path in EXAMPLES.glob("*.json")}
    require_complete_contract_set(set(schemas), set(examples))

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
        test_rejects_missing_contract_pair()
        test_rejects_unknown_rule_regime()
        count = validate_examples()
    except (OSError, ValueError, SchemaError, ValidationError) as error:
        print(f"Contract validation failed: {error}", file=sys.stderr)
        return 1
    print("Validator mismatch check passed.")
    print("Validator required-contract check passed.")
    print(f"Validated {count} contract examples against their schemas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
