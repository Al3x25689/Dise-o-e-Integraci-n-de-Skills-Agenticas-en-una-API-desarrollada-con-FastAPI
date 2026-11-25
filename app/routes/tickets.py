from fastapi import APIRouter

from app.config.rules import CATEGORY_RULES, PRIORITY_CATALOG
from app.models.tickets import CategoryDefinition, PriorityCatalog, TicketAnalysis, TicketRequest
from app.routes.errors import ANALYSIS_ERRORS
from app.services.ticket_analyzer import analyze

router = APIRouter(prefix="/tickets", tags=["Incidencias"])


@router.post("/analyze", summary="Analizar una incidencia", responses=ANALYSIS_ERRORS)
def analyze_ticket(ticket: TicketRequest) -> TicketAnalysis:
    """Clasifica y prioriza una incidencia. Devuelve una justificación y acciones iniciales."""
    return analyze(ticket)


@router.get("/categories", summary="Consultar las categorías")
def categories() -> list[CategoryDefinition]:
    """Devuelve las categorías en el orden de precedencia."""
    return [category for category, _, _ in CATEGORY_RULES]


@router.get("/priorities", summary="Consultar las reglas de prioridad")
def priorities() -> PriorityCatalog:
    """Publica los niveles, la matriz base y la prioridad mínima para Seguridad."""
    return PRIORITY_CATALOG
