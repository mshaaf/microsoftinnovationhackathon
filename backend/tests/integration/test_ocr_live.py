import os
from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parents[3] / "fixtures" / "letters"
PNG = (FIXTURES / "L01.png").read_bytes()


@pytest.mark.live
@pytest.mark.skipif(
    os.getenv("APP_MODE") != "live" or not os.getenv("AZURE_AI_SERVICES_ENDPOINT"),
    reason="requires configured Azure Document Intelligence",
)
async def test_live_l01():
    from app.adapters.ocr.live import Adapter

    result = await Adapter().read(PNG, "L01.png")
    assert "SAMPLE" in result.text and result.pages >= 1
    assert 0 <= result.confidence <= 1
