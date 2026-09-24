import re

from app.adapters.base import ServiceStatus
from app.adapters.pii.base import PiiAdapter, PiiEntity
from app.adapters.pii.redaction import fallback_entities, unique_entities
from app.core.pii import fixture_fake_pii


class Adapter(PiiAdapter):
    def health_status(self) -> ServiceStatus:
        return "mock"

    def entities(self, text: str, language: str = "en") -> tuple[PiiEntity, ...]:
        del language
        entities = list(fallback_entities(text))
        for value in fixture_fake_pii():
            category = next(
                (
                    entity.category
                    for entity in fallback_entities(value)
                    if entity.offset == 0 and entity.length == len(value)
                ),
                "Person",
            )
            entities.extend(
                PiiEntity(category, match.start(), match.end() - match.start())
                for match in re.finditer(re.escape(value), text, re.IGNORECASE)
            )
        return unique_entities(entities)
