from datetime import date
from importlib import import_module, util

import pytest

from app.core.clock import use_today


def compute(letter_date: date, regime: dict, *, lang: str = "en"):
    spec = util.find_spec("app.features.deadline.service")
    assert spec is not None, "deadline service should implement compute_deadline"
    service = import_module("app.features.deadline.service")
    return service.compute_deadline(letter_date, regime, lang=lang)


@pytest.mark.parametrize(
    (
        "letter_date",
        "today",
        "window_days",
        "appeal_due",
        "days_left",
        "rule",
    ),
    [
        (
            date(2026, 9, 15),
            date(2026, 9, 25),
            60,
            date(2026, 11, 14),
            50,
            "Within 60 days of the date on your letter.",
        ),
        (
            date(2026, 1, 31),
            date(2026, 2, 1),
            60,
            date(2026, 4, 1),
            59,
            "Within 60 days of the date on your letter.",
        ),
        (
            date(2024, 2, 29),
            date(2024, 2, 29),
            60,
            date(2024, 4, 29),
            60,
            "Within 60 days of the date on your letter.",
        ),
        (
            date(2026, 9, 15),
            date(2026, 9, 15),
            30,
            date(2026, 10, 15),
            30,
            "Within 30 days of the date on your letter.",
        ),
        (
            date(2026, 9, 15),
            date(2026, 11, 14),
            60,
            date(2026, 11, 14),
            0,
            "Within 60 days of the date on your letter.",
        ),
    ],
)
def test_deadline_uses_regime_window_and_injectable_clock(
    letter_date, today, window_days, appeal_due, days_left, rule
):
    with use_today(today):
        result = compute(letter_date, {"appeal_window_days": window_days})

    assert result.appeal_due == appeal_due
    assert result.days_left == days_left
    assert result.rule == rule


def test_past_due_deadline_points_to_fema_helpline():
    with use_today(date(2026, 8, 1)):
        result = compute(date(2026, 6, 1), {"appeal_window_days": 60})

    assert result.appeal_due == date(2026, 7, 31)
    assert result.days_left == -1
    assert result.rule == (
        "Your 60 days may have passed. Call the FEMA Helpline to ask about your options."
    )


@pytest.mark.parametrize(
    ("today", "expected_rule"),
    [
        (
            date(2026, 9, 25),
            "Dentro de los 60 días desde la fecha de su carta.",
        ),
        (
            date(2026, 11, 15),
            "Es posible que hayan pasado los 60 días. Llame a la línea de ayuda de FEMA para preguntar por sus opciones.",
        ),
    ],
)
def test_deadline_rule_is_translated(today, expected_rule):
    with use_today(today):
        result = compute(date(2026, 9, 15), {"appeal_window_days": 60}, lang="es")

    assert result.rule == expected_rule
