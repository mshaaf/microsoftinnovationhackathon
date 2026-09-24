import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PROGRAMS_PATH = ROOT / "data/programs.json"

_SPANISH = {
    "title": {
        "fema_ihp": "Ayuda de FEMA para personas y hogares",
        "irs_relief": "Alivio tributario del IRS",
        "dua": "Asistencia por Desempleo por Desastre",
        "dsnap": "Programa de Asistencia Nutricional por Desastre",
        "sba_loan": "Préstamo por desastre de la SBA",
    },
    "how_to_apply": {
        "fema_ihp": "Solicite en DisasterAssistance.gov o llame a FEMA al 1-800-621-3362.",
        "irs_relief": "Revise los avisos actuales en IRS.gov. Si se mudó al área o vive fuera de ella, llame al 866-562-5227.",
        "dua": "Comuníquese con la oficina estatal de desempleo. Presente la solicitud pronto; pueden aceptar solicitudes tardías por una buena causa.",
        "dsnap": "Comuníquese con la agencia estatal de SNAP para preguntar si D-SNAP está abierto.",
        "sba_loan": "Conozca los préstamos por desastre en SBA.gov o llame al 1-800-659-2955.",
    },
}


@lru_cache(maxsize=1)
def _programs() -> dict[str, dict]:
    data = json.loads(PROGRAMS_PATH.read_text(encoding="utf-8"))
    return {row["id"]: row for row in data["programs"]}


def _why(program_id: str, declaration: dict, lang: str) -> str:
    english = {
        "fema_ihp": (
            "Individual Assistance is open in your county. FEMA decides what help you may receive."
            if declaration["registration_open"]
            else "The registration window may have closed. Call FEMA to ask about your options."
        ),
        "irs_relief": "Tax relief may apply automatically if the IRS has your address in a covered county. The IRS decides. If you moved into or live outside the area, call 866-562-5227.",
        "dua": "If you lost work or self-employment and cannot get regular unemployment, check with your state now. The filing window is usually 30 days from the state's announcement.",
        "dsnap": "The state must request D-SNAP and USDA must approve it. Check now; the application window is often about a week.",
        "sba_loan": (
            "This low-interest loan is optional for disasters declared on or after March 22, 2024. Applying does not affect FEMA eligibility."
            if declaration["rules_regime"] == "2024-03-22"
            else "For some types of FEMA help, an SBA loan application may be needed. Check what applies to your case."
        ),
    }
    spanish = {
        "fema_ihp": (
            "La Asistencia Individual está abierta en su condado. FEMA decide qué ayuda puede recibir."
            if declaration["registration_open"]
            else "Es posible que el plazo de inscripción haya terminado. Llame a FEMA para preguntar por sus opciones."
        ),
        "irs_relief": "El alivio tributario puede aplicarse automáticamente si el IRS tiene su dirección en un condado cubierto. El IRS decide. Si se mudó al área o vive fuera de ella, llame al 866-562-5227.",
        "dua": "Si perdió trabajo o ingresos por cuenta propia y no puede recibir el desempleo regular, consulte ahora con su estado. El plazo suele ser de 30 días desde el anuncio estatal.",
        "dsnap": "El estado debe solicitar D-SNAP y el USDA debe aprobarlo. Consulte ahora; el plazo de solicitud suele ser de una semana.",
        "sba_loan": (
            "Este préstamo de bajo interés es opcional para desastres declarados desde el 22 de marzo de 2024. Solicitarlo no afecta su elegibilidad para la ayuda de FEMA."
            if declaration["rules_regime"] == "2024-03-22"
            else "Para algunos tipos de ayuda de FEMA, puede ser necesaria una solicitud de préstamo de la SBA. Consulte qué aplica a su caso."
        ),
    }
    return (spanish if lang == "es" else english)[program_id]


def _matches(program: dict, declaration: dict, answers: dict) -> bool:
    for key, expected in program["trigger_conditions"].items():
        if key == "deadline_dates_by_disaster":
            continue
        actual = declaration.get(key, answers.get(key))
        if isinstance(expected, list):
            if actual not in expected:
                return False
        elif actual != expected:
            return False
    return True


def _tier(program: dict, declaration: dict) -> str:
    logic = program["tier_logic"]
    if "tiers_by_rules_regime" in logic:
        return logic["tiers_by_rules_regime"][declaration["rules_regime"]]
    if "open_if_registration_open" in logic:
        return (
            logic["open_if_registration_open"]
            if declaration["registration_open"]
            else logic["otherwise"]
        )
    return logic["tier"]


def _deadline_date(
    program: dict, disaster_number: int, declaration: dict
) -> str | None:
    anchor = program["deadline_anchor"]
    if anchor == "registration_deadline":
        return declaration.get("registration_deadline")
    if anchor == "deadline_dates_by_disaster":
        return program["trigger_conditions"].get(anchor, {}).get(str(disaster_number))
    return None


def build_program_cards(
    disaster_number: int, declaration: dict, answers: dict, lang: str
) -> list[dict]:
    programs = _programs()
    cards = []

    for program_id, program in programs.items():
        if not _matches(program, declaration, answers):
            continue

        tier = _tier(program, declaration)
        deadline_date = _deadline_date(program, disaster_number, declaration)

        title = _SPANISH["title"][program_id] if lang == "es" else program["title"]
        how_to_apply = (
            _SPANISH["how_to_apply"][program_id]
            if lang == "es"
            else program["how_to_apply"]
        )
        deadline = None
        if deadline_date is not None:
            if lang == "es":
                deadline_label = (
                    "Solicítelo antes del"
                    if program_id == "fema_ihp"
                    else "Fecha límite"
                )
            else:
                deadline_label = "Apply by" if program_id == "fema_ihp" else "Deadline"
            deadline = {
                "date": deadline_date,
                "label": deadline_label,
            }
        cards.append(
            {
                "program_id": program_id,
                "tier": tier,
                "title": title,
                "why": _why(program_id, declaration, lang),
                "deadline": deadline,
                "how_to_apply": how_to_apply,
                "source_url": program["source_url"],
                "last_verified": program["last_verified"],
            }
        )

    return cards
