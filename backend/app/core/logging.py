import logging

from app.core.pii import redact_text


def _redact_value(value):
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, tuple):
        return tuple(_redact_value(item) for item in value)
    if isinstance(value, list):
        return [_redact_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _redact_value(item) for key, item in value.items()}
    return value


class RedactionFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = _redact_value(record.msg)
        record.args = _redact_value(record.args)
        for key, value in record.__dict__.items():
            if key not in {"msg", "args", "exc_info"}:
                record.__dict__[key] = _redact_value(value)
        if record.exc_info:
            record.exc_text = redact_text(
                logging.Formatter().formatException(record.exc_info)
            )
            record.exc_info = None
        return True


_redaction_filter = RedactionFilter()


def install_redaction_filter() -> None:
    root = logging.getLogger()
    if not any(item is _redaction_filter for item in root.filters):
        root.addFilter(_redaction_filter)
    for handler in root.handlers:
        if not any(item is _redaction_filter for item in handler.filters):
            handler.addFilter(_redaction_filter)

    current_factory = logging.getLogRecordFactory()
    if getattr(current_factory, "_redaction_filter_installed", False):
        return

    def record_factory(*args, **kwargs):
        record = current_factory(*args, **kwargs)
        _redaction_filter.filter(record)
        return record

    record_factory._redaction_filter_installed = True
    logging.setLogRecordFactory(record_factory)
