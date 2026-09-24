from datetime import date, timedelta

from pydantic import BaseModel

from app.core.clock import today

_RULE_TEXT = {
    "en": {
        "current": "Within {days} days of the date on your letter.",
        "past_due": (
            "Your {days} days may have passed. Call the FEMA Helpline to ask about your options."
        ),
    },
    "es": {
        "current": "Dentro de los {days} días desde la fecha de su carta.",
        "past_due": (
            "Es posible que hayan pasado los {days} días. "
            "Llame a la línea de ayuda de FEMA para preguntar por sus opciones."
        ),
    },
}


class Deadline(BaseModel):
    appeal_due: date
    days_left: int
    rule: str


def compute_deadline(
    letter_date: date, regime: dict[str, int], *, lang: str = "en"
) -> Deadline:
    window_days = regime["appeal_window_days"]
    appeal_due = letter_date + timedelta(days=window_days)
    days_left = (appeal_due - today()).days
    language = lang if lang in _RULE_TEXT else "en"
    message = "past_due" if days_left < 0 else "current"

    return Deadline(
        appeal_due=appeal_due,
        days_left=days_left,
        rule=_RULE_TEXT[language][message].format(days=window_days),
    )
