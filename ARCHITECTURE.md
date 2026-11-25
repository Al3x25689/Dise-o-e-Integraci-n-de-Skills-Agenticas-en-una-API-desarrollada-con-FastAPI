# Arquitectura

Una aplicación FastAPI local recibe entradas estructuradas. Las rutas delegan el análisis a un servicio determinista. Los catálogos públicos y el servicio consultan la misma configuración.

| Ruta | Responsabilidad |
|---|---|
| `app/main.py` | Crear la aplicación y registrar los routers. Exponer Swagger en `/docs` y OpenAPI en `/openapi.json`. |
| `app/routes/health.py` | Responder al chequeo de disponibilidad. |
| `app/routes/tickets.py` | Exponer el análisis y los catálogos. |
| `app/routes/errors.py` | Unificar las respuestas HTTP 400, 404 y 422 y sus esquemas OpenAPI. |
| `app/models/tickets.py` | Definir contratos Pydantic y validar las solicitudes. |
| `app/config/rules.py` | Centralizar catálogos, coincidencias, matriz, excepción de seguridad y recomendaciones. |
| `app/services/ticket_analyzer.py` | Clasificar, calcular prioridad, justificar y seleccionar recomendaciones. |
| `tests/test_ticket_analyzer.py` | Verificar reglas y casos límite sin servidor HTTP. |
| `tests/test_api.py` | Verificar contratos HTTP y OpenAPI con pytest y TestClient. |
| `README.md`, `requirements.txt`, `requirements-dev.txt`, `.gitignore` | Documentar el uso fuera de Codex, declarar dependencias de ejecución y pruebas y excluir `.venv`. |
| `.github/agents/soporte-it.agent.md` | Definir el rol de soporte y habilitar las herramientas necesarias. |
| `.github/skills/analizar-ticket-it/SKILL.md` | Guiar la conversación y el uso del contrato HTTP local. |
| `scripts/it_support_client.py` | Consultar la API local con JSON UTF-8 desde el intérprete de `.venv`. |
| `scripts/Invoke-ItSupportApi.ps1` | Adaptador opcional para sesiones que permitan ejecutar el archivo. |

## Contratos aprobados para el diseño

| Endpoint | Entrada | Respuesta |
|---|---|---|
| `GET /health` | Sin parámetros | `200` con `status` igual a `ok`. |
| `POST /tickets/analyze` | JSON con `description`, `impact` y `urgency`, todos obligatorios. | `200` con `category` y `priority` (objetos con `code` y `label`), `reason` y `recommendations` (lista ordenada de textos). `400` si el cuerpo es ilegible o el JSON está mal formado. `422` si la entrada incumple el contrato. |
| `GET /tickets/categories` | Sin parámetros | `200` con el catálogo de códigos, etiquetas y descripciones. |
| `GET /tickets/priorities` | Sin parámetros | `200` con los niveles y definiciones de impacto, urgencia y prioridad, las nueve combinaciones de la matriz base y la excepción de seguridad. |

El catálogo usa `impact_levels`, `urgency_levels`, `priority_levels`, `matrix` y `security_exception`. Las rutas inexistentes devuelven `404`. Los errores `400`, `404` y `422` comparten una lista `detail` con `type`, `loc` y `msg` en cada elemento. Consulta [las reglas aprobadas](docs/REGLAS_NEGOCIO.md) para la validación y el análisis.

## Integración local

Abre el repositorio en VS Code, elige una sesión local de Copilot y selecciona **Soporte IT**. La skill guía la invocación directa del cliente Python con `.venv` para consultar la API en `http://127.0.0.1:8000`. El agente respeta las confirmaciones de VS Code. Los resultados manuales informados figuran en el [registro de evidencias](docs/EVIDENCIAS_IA.md).
