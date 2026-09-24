import pytest
from fastapi.testclient import TestClient

from app.adapters import get_adapter
from app.adapters.search.chunking import MAX_CHARS, chunk_markdown, load_kb
from app.main import app

DOC = """---
url: https://www.fema.gov/x
title: T
agency: FEMA
lang: en
topic: appeals
fetched_at: 2026-09-23
---
## One
short

## Two
""" + ("word " * 500)


def test_chunker_splits_on_headings_caps_size_and_keeps_metadata():
    chunks = chunk_markdown(DOC)
    assert len(chunks) >= 3
    assert all(len(c["content"]) <= MAX_CHARS for c in chunks)
    assert all(
        c["url"] == "https://www.fema.gov/x" and c["agency"] == "FEMA" for c in chunks
    )
    assert len({c["id"] for c in chunks}) == len(chunks)


def test_chunker_rejects_missing_front_matter():
    with pytest.raises(ValueError):
        chunk_markdown("## no front matter")
    with pytest.raises(ValueError):
        chunk_markdown(DOC.replace("topic: appeals\n", ""))


def test_kb_files_are_valid_and_https():
    chunks = load_kb()
    assert chunks
    assert all(c["url"].startswith("https://") for c in chunks)


def test_mock_search_returns_url_bearing_results():
    results = get_adapter("search", "mock").search("appeal")
    assert results
    assert all(r["url"].startswith("https://") and r["content"] for r in results)


def test_debug_search_endpoint(monkeypatch):
    client = TestClient(app)
    r = client.get("/api/debug/search", params={"q": "appeal"})
    assert r.status_code == 200 and r.json()["results"]
    monkeypatch.setenv("APP_ENV", "prod")
    assert client.get("/api/debug/search", params={"q": "appeal"}).status_code == 404
