import os

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.mark.live
@pytest.mark.skipif(
    os.getenv("APP_MODE", "mock") != "live", reason="requires live OpenFEMA access"
)
def test_live_demo_county_has_disaster_4936():
    response = TestClient(app).get(
        "/api/declarations?state=HI&county_fips=15001&lang=en"
    )

    assert response.status_code == 200
    assert any(
        row["disaster_number"] == 4936 for row in response.json()["declarations"]
    )
