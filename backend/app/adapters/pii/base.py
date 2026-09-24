from dataclasses import dataclass

from app.adapters.base import BaseAdapter, NotConfigured, ServiceStatus


@dataclass(frozen=True)
class PiiEntity:
    category: str
    offset: int
    length: int


class PiiAdapter(BaseAdapter):
    def entities(self, text: str, language: str = "en") -> tuple[PiiEntity, ...]:
        raise NotImplementedError

    def detect(self, text: str, language: str = "en") -> tuple[str, ...]:
        # Import here because redaction.py uses PiiEntity from this module.
        from app.adapters.pii.redaction import fallback_entities, unique_entities

        entities = unique_entities(
            (*self.entities(text, language), *fallback_entities(text))
        )
        return tuple(dict.fromkeys(entity.category for entity in entities))


__all__ = ["NotConfigured", "PiiAdapter", "PiiEntity", "ServiceStatus"]
