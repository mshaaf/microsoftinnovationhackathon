import re
from pathlib import Path

DIRECT_MODEL_IMPORT = re.compile(
    r"(?:\b(?:from|import)\s+[.\w]*adapters\.model(?:\.|\s|$)"
    r"|\bfrom\s+app\.adapters\s+import\s+[^#\n]*\bmodel\b"
    r"|\bget_adapter\(\s*(?:service\s*=\s*)?['\"]model['\"])"
)
APP = Path(__file__).resolve().parents[1] / "app"


def test_app_modules_do_not_import_model_adapter_outside_gateway():
    violations = [
        f"{path}:{line_number}"
        for path in APP.rglob("*.py")
        if path.relative_to(APP).as_posix() != "core/model_gateway.py"
        and path.relative_to(APP).parts[:2] != ("adapters", "model")
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        )
        if DIRECT_MODEL_IMPORT.search(line)
    ]

    assert not violations, "Use core.model_gateway for model calls: " + ", ".join(
        violations
    )
