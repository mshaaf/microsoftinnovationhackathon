from datetime import date

from app.core.clock import today, use_today


def test_today_uses_scoped_override_and_restores_default():
    before = today()

    with use_today(date(2026, 9, 25)):
        assert today() == date(2026, 9, 25)

    assert today() == before
