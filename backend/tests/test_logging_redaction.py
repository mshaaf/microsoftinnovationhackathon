import logging

from uvicorn.logging import AccessFormatter

from app.core import pii
from app.main import create_app


def test_app_logging_redacts_fixture_pii_phone_and_registration_number(
    monkeypatch, caplog
):
    monkeypatch.setattr(pii, "fixture_fake_pii", lambda: ("Jordan Samplewell",))
    create_app()
    logger = logging.getLogger("privacy-redaction-test")

    with caplog.at_level(logging.WARNING):
        logger.warning(
            "contact %s, phone %s, cell %s, registration %s",
            "Jordan Samplewell",
            "555-0142",
            "5550142678",
            "987654321",
        )

    assert "Jordan Samplewell" not in caplog.text
    assert "555-0142" not in caplog.text
    assert "5550142678" not in caplog.text
    assert "987654321" not in caplog.text
    assert "[REDACTED" in caplog.text


def test_redaction_preserves_uvicorn_access_log_arguments():
    create_app()
    record = logging.getLogRecordFactory()(
        "uvicorn.access",
        logging.INFO,
        __file__,
        0,
        '%s - "%s %s HTTP/%s" %d',
        ("127.0.0.1", "GET", "/api/health", "1.1", 200),
        None,
    )

    formatted = AccessFormatter(
        '%(client_addr)s "%(request_line)s" %(status_code)s', use_colors=False
    ).format(record)

    assert formatted == '127.0.0.1 "GET /api/health HTTP/1.1" 200 OK'
