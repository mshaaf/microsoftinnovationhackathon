import json
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI

from evals.run import run_evaluations


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
