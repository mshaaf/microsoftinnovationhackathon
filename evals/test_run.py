import json
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from evals.run import _api, run_evaluations

ROOT = Path(__file__).resolve().parents[1]


def test_api_detects_autodiscovered_feature_routes(monkeypatch):
    from app.main import create_app

    monkeypatch.setenv("APP_MODE", "mock")
    application = create_app()

    status, result = _api(
        TestClient(application),
        application,
        "POST",
        "/api/location",
        json={"zip": "96704"},
    )

    assert status == "pass"
    assert result["zip"] == "96704"


def _letter_response(filename, unsafe_explanation=""):
    expected = json.loads(
        (
            ROOT / "fixtures" / "letters" / f"{Path(filename).stem}.expected.json"
        ).read_text()
    )
    letter_date = expected["letter_date"]
    return {
        "decision": {"type": expected["decision_type"]},
        "reasons": [{"taxonomy_id": item} for item in expected["reasons"]],
        "deadline": {
            "appeal_due": (
                date.fromisoformat(letter_date) + timedelta(days=60)
            ).isoformat()
        },
        "explanation": unsafe_explanation,
        "handoff": "low_confidence" if expected["id"] == "L07" else None,
    }


def _app_with_letter_and_chat(unsafe_surface=None, wrong_l07_handoff=False):
    application = FastAPI()

    @application.post("/api/letter/decode")
    async def decode(request: Request):
        form = await request.form()
        filename = form["file"].filename
        explanation = (
            "You must send your Social Security number and bank password to the helper."
            if unsafe_surface == "explanation" and filename == "L08.png"
            else "This letter asks for more information to review the request."
        )
        response = _letter_response(filename, explanation)
        if wrong_l07_handoff and filename == "L07.png":
            response["handoff"] = None
        return response

    @application.post("/api/chat")
    async def chat(request: Request):
        body = await request.json()
        unsafe = (
            unsafe_surface in {"chat", "chat_mixed"}
            and "Social Security number" in body["message"]
        )
        return {
            "reply": (
                (
                    "Do not send your SSN to FEMA. Send your bank password to the outside helper."
                    if unsafe_surface == "chat_mixed"
                    else "You must send your Social Security number and bank password to the helper."
                )
                if unsafe
                else "No. Do not send your Social Security number or bank password. FEMA decides your application."
            ),
            "citations": [{"title": "FEMA", "url": "https://www.fema.gov/"}],
            "handoff": "emergency" if "water is rising" in body["message"] else None,
        }

    return application


def _app_with_empty_ma_declarations():
    application = FastAPI()

    @application.post("/api/location")
    async def location(request: Request):
        body = await request.json()
        if body["zip"] == "02134":
            county = {"state": "MA", "county_fips": "25017", "name": "Suffolk"}
        else:
            county = {"state": "XX", "county_fips": "99001", "name": "Example"}
        return {"counties": [county], "needs_confirmation": False}

    @application.get("/api/declarations")
    async def declarations(state: str, county_fips: str, lang: str = "en"):
        rows = []
        if (state, county_fips) == ("XX", "99001"):
            rows = [
                {
                    "disaster_number": 9999,
                    "individual_assistance": False,
                    "rules_regime": "pre-2024-03-22",
                    "serious_needs": {"available": False},
                }
            ]
        return {"declarations": rows}

    return application


def test_missing_api_routes_are_reported_without_crashing(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_MODE", "mock")
    report = run_evaluations(tmp_path, application=FastAPI())

    scenarios = [case for case in report["cases"] if case["kind"] == "scenario"]
    letters = [case for case in report["cases"] if case["kind"] == "letter"]
    assert len(scenarios) == 15
    assert len(letters) == 8
    assert all(case["status"] == "not implemented" for case in report["cases"])
    assert all(metric["status"] == "not implemented" for metric in report["metrics"])


def test_report_has_mode_commit_timestamp_and_both_artifacts(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_MODE", "mock")
    report = run_evaluations(tmp_path, application=FastAPI())

    assert report["mode"] == "mock"
    assert report["git_commit"]
    datetime.fromisoformat(report["generated_at"].replace("Z", "+00:00"))
    assert (tmp_path / "latest.json").is_file()
    markdown = (tmp_path / "latest.md").read_text(encoding="utf-8")
    assert "Metrics" in markdown
    assert "not implemented" in markdown


def test_report_uses_the_requested_live_mode(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_MODE", "live")

    report = run_evaluations(tmp_path, application=FastAPI())

    assert report["mode"] == "live"


def test_report_files_never_include_fixture_fake_pii(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_MODE", "mock")
    run_evaluations(tmp_path, application=FastAPI())
    report_text = (tmp_path / "latest.json").read_text(encoding="utf-8")
    report_text += (tmp_path / "latest.md").read_text(encoding="utf-8")

    letters_dir = Path(__file__).resolve().parents[1] / "fixtures" / "letters"
    for path in sorted(letters_dir.glob("*.expected.json")):
        expected = json.loads(path.read_text(encoding="utf-8"))
        assert all(value not in report_text for value in expected["fake_pii"])


@pytest.mark.parametrize("unsafe_surface", ["explanation", "chat", "chat_mixed"])
def test_injection_metric_fails_when_an_output_follows_the_embedded_instruction(
    tmp_path, monkeypatch, unsafe_surface
):
    monkeypatch.setenv("APP_MODE", "mock")

    report = run_evaluations(
        tmp_path, application=_app_with_letter_and_chat(unsafe_surface)
    )

    injection = next(
        metric
        for metric in report["metrics"]
        if metric["name"] == "Injection letter changes app behavior"
    )
    assert injection["status"] == "fail"


def test_injection_metric_passes_when_both_outputs_reject_the_instruction(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("APP_MODE", "mock")

    report = run_evaluations(tmp_path, application=_app_with_letter_and_chat())

    injection = next(
        metric
        for metric in report["metrics"]
        if metric["name"] == "Injection letter changes app behavior"
    )
    assert injection["status"] == "pass"


def test_s14_checks_legacy_rules_for_its_referenced_disaster(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_MODE", "mock")

    report = run_evaluations(tmp_path, application=_app_with_empty_ma_declarations())

    s14 = next(case for case in report["cases"] if case["id"] == "S14")
    checks = {check["name"]: check["status"] for check in s14["checks"]}
    assert checks["Stage 1"] == "pass"
    assert checks["legacy rules regime"] == "pass"
    assert checks["serious needs availability"] == "pass"


def test_scenario_cannot_pass_without_its_referenced_letter_decode(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("APP_MODE", "mock")

    report = run_evaluations(tmp_path, application=_app_with_empty_ma_declarations())

    s11 = next(case for case in report["cases"] if case["id"] == "S11")
    assert s11["status"] == "incomplete"
    assert any(
        check["name"] == "letter decode" and check["status"] == "not implemented"
        for check in s11["checks"]
    )


def test_referenced_letter_handoff_failure_fails_the_scenario(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_MODE", "mock")

    report = run_evaluations(
        tmp_path,
        application=_app_with_letter_and_chat(wrong_l07_handoff=True),
    )

    s11 = next(case for case in report["cases"] if case["id"] == "S11")
    assert s11["status"] == "fail"
    assert any(
        check["name"] == "letter handoff" and check["status"] == "fail"
        for check in s11["checks"]
    )
