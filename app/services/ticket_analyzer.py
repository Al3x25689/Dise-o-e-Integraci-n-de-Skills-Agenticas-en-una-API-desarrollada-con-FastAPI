import re
import unicodedata

from app.config.rules import CATEGORY_RULES, MATRIX, PRIORITY_CATALOG
from app.models.tickets import Category, Priority, TicketAnalysis, TicketRequest


def normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.casefold())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


CLASSIFIERS = [
    (category, re.compile(r"(?<!\w)(?:" + "|".join(
        re.escape(normalize(term)) for term in terms
    ) + r")(?!\w)"), recommendations)
    for category, terms, recommendations in CATEGORY_RULES if terms
]
PRIORITIES = {definition.code: definition for definition in PRIORITY_CATALOG.priority_levels}
PRIORITY_ORDER = list(PRIORITIES)


def analyze(ticket: TicketRequest) -> TicketAnalysis:
    normalized = normalize(ticket.description)
    category, _, recommendations = CATEGORY_RULES[-1]
    classification_reason = "Sin coincidencias en el vocabulario."
    for candidate, pattern, actions in CLASSIFIERS:
        match = pattern.search(normalized)
        if match:
            category, recommendations = candidate, actions
            classification_reason = f"Coincidencia con «{match.group()}» en {category.label}."
            break

    base_code = MATRIX[ticket.impact, ticket.urgency]
    priority_code = base_code
    exception = PRIORITY_CATALOG.security_exception
    if category.code == exception.category:
        priority_code = max(base_code, exception.minimum_priority, key=PRIORITY_ORDER.index)

    priority = PRIORITIES[priority_code]
    reason = (
        f"{classification_reason} La matriz de impacto {ticket.impact} "
        f"y urgencia {ticket.urgency} indica prioridad {PRIORITIES[base_code].label}."
    )
    if priority_code != base_code:
        reason += f" Se aplica la prioridad mínima de Seguridad ({priority.label})."

    return TicketAnalysis(
        category=Category(code=category.code, label=category.label),
        priority=Priority(code=priority.code, label=priority.label),
        reason=reason,
        recommendations=[*recommendations, priority.description],
    )
