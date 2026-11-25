# IT Support API

Proyecto académico individual de Kodigo — Diseño e integración de skills agénticas en una API con FastAPI. Su objetivo es clasificar incidencias informáticas ficticias, calcular su prioridad y devolver justificaciones y recomendaciones mediante reglas deterministas.

## Arquitectura

La API separa rutas (`app/routes/`), contratos Pydantic (`app/models/`), reglas de negocio (`app/config/`) y lógica de análisis (`app/services/`). El agente **Soporte IT** interpreta la solicitud y utiliza la skill `analizar-ticket-it` para consultar la API mediante `scripts/it_support_client.py`. La decisión final de clasificación y prioridad corresponde a la API, no al modelo de IA.

**Flujo:** Usuario → Copilot / Soporte IT → Skill → Cliente Python → FastAPI → Servicio de análisis → Respuesta al usuario.

## Instalación y ejecución

Desde la raíz del repositorio, en Windows PowerShell con Python de 64 bits (verificado originalmente con CPython 3.14.10):

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abre [Swagger UI](http://127.0.0.1:8000/docs) o el [esquema OpenAPI](http://127.0.0.1:8000/openapi.json).

| Método y ruta | Función |
|---|---|
| `GET /health` | Verificar disponibilidad. |
| `GET /tickets/categories` | Consultar las siete categorías. |
| `GET /tickets/priorities` | Consultar niveles, matriz y excepción de Seguridad. |
| `POST /tickets/analyze` | Clasificar y priorizar una incidencia. |

Ejemplo de POST en Swagger (Try it out → Execute):

```json
{"description":"La impresora de mi puesto no imprime.","impact":"low","urgency":"low"}
```

Resultado esperado: Hardware, prioridad Baja. Los errores HTTP 400, 404 y 422 comparten el formato `detail` con `type`, `loc` y `msg`.

## Integración agéntica

Abre el repositorio en VS Code con GitHub Copilot, inicia la API y selecciona el [agente Soporte IT](.github/agents/soporte-it.agent.md). La [skill](.github/skills/analizar-ticket-it/SKILL.md) guía la recopilación de datos, la consulta HTTP y la presentación del resultado. Si faltan datos, solicita aclaraciones; si la API falla, no inventa una clasificación. Las consultas generales quedan fuera de su alcance. El cliente Python utiliza la biblioteca estándar y UTF-8 explícito, sin modificar políticas de ejecución de PowerShell.

## Evidencias y validación

| Evidencia | Resultado observado |
|---|---|
| [01 — Swagger](docs/evidencias/01-swagger.png) | Cuatro endpoints documentados. |
| [02 — Skill detectada](docs/evidencias/02-skill-detectada.png) | `analizar-ticket-it` disponible en Copilot. |
| [03 — Impresora](docs/evidencias/03-impresora-prioridad-baja.png) | Hardware / Baja. |
| [04 — Facturación](docs/evidencias/04-facturacion-prioridad-critica.png) | Sistemas empresariales / Crítica. |
| [05 — Phishing](docs/evidencias/05-phishing-prioridad-alta.png) | Seguridad / Alta por excepción. |
| [06 — Información insuficiente](docs/evidencias/06-informacion-insuficiente.png) | Solicita aclaración antes de analizar. |
| [07 — Fuera de alcance](docs/evidencias/07-consulta-fuera-de-alcance.png) | Responde una consulta general sin usar la API. |
| [08 — API no disponible](docs/evidencias/08-api-no-disponible.png) | Comunica el bloqueo sin inventar resultados. |
| [09 — Sin skill](docs/evidencias/09-comparacion-sin-skill.png) | Ensayo histórico con consultas adicionales a archivos. |
| [10 — pytest](docs/evidencias/10-pruebas-automatizadas.png) | 59 aprobadas, 0 fallidas, 1 advertencia; 1.48 s. |

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

El ensayo histórico sin skill tardó 73 segundos según el registro manual; no constituye una medición controlada, pues también cambió el cliente HTTP. La advertencia de pytest corresponde a la deprecación de HTTPX con TestClient de Starlette. El uso de IA, las decisiones humanas y las incidencias técnicas se documentan en [EVIDENCIAS_IA.md](docs/EVIDENCIAS_IA.md). Consulta también [ARCHITECTURE.md](ARCHITECTURE.md) y [REGLAS_NEGOCIO.md](docs/REGLAS_NEGOCIO.md).
