import re
from html import escape

GLOSSARY = {
    "FEMA": "FEMA",
    "Individual Assistance": "Asistencia Individual",
    "Serious Needs Assistance": "Asistencia por Necesidades Graves",
    "Disaster Recovery Center": "Centro de Recuperación por Desastre",
    "appeal": "apelación",
}
_GLOSSARY_PATTERN = re.compile(
    "|".join(re.escape(term) for term in sorted(GLOSSARY, key=len, reverse=True)),
    re.IGNORECASE,
)
_GLOSSARY_CASEFOLD = {
    term.casefold(): translation for term, translation in GLOSSARY.items()
}


def translator_text(text: str) -> str:
    escaped = escape(text, quote=False)
    return _GLOSSARY_PATTERN.sub(
        lambda match: (
            f'<mstrans:dictionary translation="{_GLOSSARY_CASEFOLD[match[0].casefold()]}">'
            f"{match[0]}</mstrans:dictionary>"
        ),
        escaped,
    )
