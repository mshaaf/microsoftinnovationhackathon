from app.adapters.base import ServiceStatus

from .base import TranslatorAdapter

TRANSLATION_FIXTURES = {
    "Common disaster-related rumors: FEMA never charges fees.": (
        "Rumores comunes: FEMA nunca cobra tarifas."
    ),
    "Si no está de acuerdo con la decisión de FEMA (apelaciones): Su número de solicitud de FEMA y el número del desastre en cada página. La carta de FEMA indica qué documentos necesita para su caso.": (
        "Incluya el número de solicitud de FEMA y el número del desastre en cada página. La carta de FEMA indica qué documentos necesita para su caso."
    ),
}


class Adapter(TranslatorAdapter):
    def health_status(self) -> ServiceStatus:
        return "mock"

    def translate(self, text: str) -> str:
        return TRANSLATION_FIXTURES.get(text, f"[es] {text}")
