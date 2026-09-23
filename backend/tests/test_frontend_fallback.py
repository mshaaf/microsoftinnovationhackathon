from fastapi.testclient import TestClient

from app import main


def test_frontend_assets_and_spa_routes_are_served(tmp_path, monkeypatch):
    (tmp_path / "index.html").write_text("<main>Navigator</main>", encoding="utf-8")
    assets = tmp_path / "assets"
    assets.mkdir()
    (assets / "app.js").write_text("window.ready = true", encoding="utf-8")
    monkeypatch.setattr(main, "FRONTEND_DIST", tmp_path)

    client = TestClient(main.create_app())

    assert client.get("/").text == "<main>Navigator</main>"
    assert client.get("/assets/app.js").text == "window.ready = true"
    assert client.get("/stage/three").text == "<main>Navigator</main>"
