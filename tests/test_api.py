import json
import re
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
VALID = {"description": "Falla la impresora", "impact": "low", "urgency": "high"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_categories():
    response = client.get("/tickets/categories")
    assert response.status_code == 200
    categories = response.json()
    assert [item["code"] for item in categories] == [
        "security", "access", "network", "business_systems", "hardware", "software", "other",
    ]
    assert all(item["description"] for item in categories)


def test_analysis():
    response = client.post("/tickets/analyze", json=VALID)
    assert response.status_code == 200
    result = response.json()
    assert result["category"] == {"code": "hardware", "label": "Hardware"}
    assert result["priority"] == {"code": "medium", "label": "Media"}
    assert result["reason"]
    assert result["recommendations"][-1] == "Programar la atención según disponibilidad."


def test_utf8_round_trip():
    payload = {
        "description": 'El ERP mostró «Error de facturación» al abrir "Información" 💡.',
        "impact": "high",
        "urgency": "high",
    }
    response = client.post(
        "/tickets/analyze",
        content=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    assert response.status_code == 200
    body = json.loads(response.content.decode("utf-8", errors="strict"))
    assert body["category"]["label"] == "Sistemas empresariales"
    assert body["priority"]["label"] == "Crítica"
    assert "procedimiento de incidentes críticos" in body["recommendations"][-1]
    assert "Crítica".encode("utf-8") in response.content


@pytest.mark.parametrize(
    "body",
    [
        b'{"description":"Conexi\xf3n perdida"}',
        b'{"description": "Falla la impresora",}',
    ],
)
def test_invalid_json_returns_400(body):
    response = client.post(
        "/tickets/analyze", content=body, headers={"Content-Type": "application/json; charset=utf-8"},
    )
    assert response.status_code == 400
    item, = json.loads(response.content.decode("utf-8"))["detail"]
    assert set(item) == {"type", "loc", "msg"}
    assert item["type"] == "invalid_json"
    assert item["loc"][0] == "body"


def test_unknown_route_returns_404():
    response = client.get("/tickets/inexistente")
    assert response.status_code == 404
    assert json.loads(response.content.decode("utf-8")) == {
        "detail": [{"type": "not_found", "loc": ["path"], "msg": "La ruta solicitada no existe."}],
    }


def test_priority_catalog_agrees_with_analysis():
    response = client.get("/tickets/priorities")
    assert response.status_code == 200
    catalog = response.json()
    for field in ("impact_levels", "urgency_levels"):
        assert [item["code"] for item in catalog[field]] == ["low", "medium", "high"]
        assert all(item["description"] for item in catalog[field])
    assert [item["code"] for item in catalog["priority_levels"]] == [
        "low", "medium", "high", "critical",
    ]
    assert catalog["security_exception"] == {"category": "security", "minimum_priority": "high"}
    matrix = catalog["matrix"]
    assert len(matrix) == 9
    assert {(cell["impact"], cell["urgency"]) for cell in matrix} == {
        (impact, urgency) for impact in ("low", "medium", "high")
        for urgency in ("low", "medium", "high")
    }
    for cell in matrix:
        payload = {**VALID, "impact": cell["impact"], "urgency": cell["urgency"]}
        normal = client.post("/tickets/analyze", json=payload)
        assert normal.status_code == 200
        assert normal.json()["priority"]["code"] == cell["priority"]
        security = client.post("/tickets/analyze", json={**payload, "description": "Alerta de malware"})
        assert security.status_code == 200
        expected = "critical" if cell["priority"] == "critical" else "high"
        assert security.json()["priority"]["code"] == expected


@pytest.mark.parametrize("size", [5, 2000])
def test_description_accepts_boundaries_after_trimming(size):
    response = client.post("/tickets/analyze", json={**VALID, "description": "  " + "x" * size + "  "})
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("description", ""), ("description", "    "), ("description", "  abcd  "),
        ("description", "x" * 2001), ("description", 12345), ("description", None),
        ("description", ["texto"]), ("description", {"texto": "prueba"}),
        ("impact", "HIGH"), ("impact", 1), ("impact", False),
        ("urgency", "critical"), ("urgency", ["high"]), ("urgency", None),
        ("unknown", "extra"),
    ],
)
def test_invalid_fields(field, value):
    response = client.post("/tickets/analyze", json={**VALID, field: value})
    assert response.status_code == 422
    item, = response.json()["detail"]
    assert set(item) == {"type", "loc", "msg"}
    assert item["loc"] == ["body", field]


@pytest.mark.parametrize("field", ["description", "impact", "urgency"])
def test_missing_fields(field):
    payload = VALID.copy()
    del payload[field]
    response = client.post("/tickets/analyze", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", field]


def test_openapi_and_swagger():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert set(schema["paths"]) == {"/health", "/tickets/analyze", "/tickets/categories", "/tickets/priorities"}
    errors = schema["paths"]["/tickets/analyze"]["post"]["responses"]
    for status in ("400", "404", "422"):
        assert errors[status]["content"]["application/json"]["schema"] == {
            "$ref": "#/components/schemas/ErrorResponse",
        }
    request = schema["components"]["schemas"]["TicketRequest"]
    assert set(request["required"]) == {"description", "impact", "urgency"}
    assert request["additionalProperties"] is False
    assert client.get("/docs").status_code == 200


def test_skill_structure():
    folder = Path(__file__).resolve().parents[1] / ".github/skills/analizar-ticket-it"
    parts = (folder / "SKILL.md").read_text(encoding="utf-8").split("---", 2)
    assert len(parts) == 3 and parts[0] == ""
    metadata = yaml.safe_load(parts[1])
    assert metadata["name"] == folder.name
    assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata["name"])
    assert len(metadata["name"]) <= 64
    assert 1 <= len(metadata["description"].strip()) <= 1024
    assert all(title in parts[2] for title in ("Formato de salida", "criterios de terminado", "Ejemplos"))
