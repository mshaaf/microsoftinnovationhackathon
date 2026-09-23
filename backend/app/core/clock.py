from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import date, datetime

_today_override: ContextVar[date | None] = ContextVar("today_override", default=None)


def today() -> date:
    return _today_override.get() or datetime.now().astimezone().date()


@contextmanager
def use_today(value: date) -> Iterator[None]:
    token = _today_override.set(value)
    try:
        yield
    finally:
        _today_override.reset(token)
