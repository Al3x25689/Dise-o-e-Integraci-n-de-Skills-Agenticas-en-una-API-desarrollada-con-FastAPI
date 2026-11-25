import pytest

from app.models.tickets import TicketRequest
from app.services.ticket_analyzer import analyze


@pytest.mark.parametrize(
    ("description", "expected"),
    [
        ("Detecté ransomware", "security"),
        ("Olvidé la CONTRASEÑA", "access"),
        ("Falla el Wi-Fi", "network"),
        ("Falló la FACTURACION", "business_systems"),
        ("El teclado no responde", "hardware"),
        ("La APLICACION se cierra", "software"),
        ("Comportamiento intermitente sin más detalles", "other"),
        ("Estoy alrededor del edificio", "other"),
        ("El supermonitor vibra", "other"),
        ("No hay malware, solo falla el monitor", "security"),
        ("Correo sospechoso y cuenta bloqueada", "security"),
        ("Falla la VPN al iniciar sesion", "access"),
        ("SAP se desconecta de la red", "network"),
        ("El ERP falla con la impresora", "business_systems"),
        ("El monitor falla al abrir Word", "hardware"),
        ("Detecté un VIRUS INFORMA\u0301TICO", "security"),
    ],
)
def test_classification(description, expected):
    result = analyze(TicketRequest(description=description, impact="low", urgency="low"))
    assert result.category.code == expected
    assert result.reason


@pytest.mark.parametrize(
    ("impact", "urgency", "expected"),
    [
        ("low", "low", "low"),
        ("low", "medium", "low"),
        ("low", "high", "medium"),
        ("medium", "low", "low"),
        ("medium", "medium", "medium"),
        ("medium", "high", "high"),
        ("high", "low", "medium"),
        ("high", "medium", "high"),
        ("high", "high", "critical"),
    ],
)
def test_matrix(impact, urgency, expected):
    result = analyze(TicketRequest(description="Falló la impresora", impact=impact, urgency=urgency))
    assert result.priority.code == expected
    assert result.recommendations[0] == "Comprobar las conexiones físicas."


@pytest.mark.parametrize(
    ("impact", "urgency", "expected", "raised"),
    [
        ("low", "low", "high", True),
        ("medium", "medium", "high", True),
        ("medium", "high", "high", False),
        ("high", "high", "critical", False),
    ],
)
def test_security_exception(impact, urgency, expected, raised):
    result = analyze(TicketRequest(description="Detecté PHÍSHING", impact=impact, urgency=urgency))
    assert result.priority.code == expected
    assert ("prioridad mínima" in result.reason) is raised
    assert "Conservar las evidencias." in result.recommendations
    if expected == "critical":
        assert result.recommendations[-1].startswith("Notificar inmediatamente")
    else:
        assert result.recommendations[-1] == "Escalar al equipo responsable para atención prioritaria."
