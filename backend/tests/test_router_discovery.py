from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import register_feature_routers


def test_probe_feature_router_is_discovered(tmp_path, monkeypatch):
    package_name = "probe_features"
    package = tmp_path / package_name
    feature = package / "_probe"
    feature.mkdir(parents=True)
    (package / "__init__.py").touch()
    (feature / "__init__.py").touch()
    (feature / "router.py").write_text(
        "from fastapi import APIRouter\n"
        "router = APIRouter()\n"
        "@router.get('/probe')\n"
        "def probe():\n"
        "    return {'discovered': True}\n",
        encoding="utf-8",
    )
    monkeypatch.syspath_prepend(str(tmp_path))

    app = FastAPI()
    register_feature_routers(app, package_name)

    response = TestClient(app).get("/api/probe")
    assert response.status_code == 200
    assert response.json() == {"discovered": True}
