# Registro de trabajo con IA

| Etapa | Aporte de IA | Decisión humana registrada |
|---|---|---|
| Diseño inicial | Propuso módulos, contratos preliminares, integración local y estrategia de pruebas. | Se aprobaron la arquitectura modular, los cuatro endpoints, los contratos preliminares y el uso de Copilot local. |
| Definición de reglas | Organizó en documentos las decisiones recibidas y propuso términos y recomendaciones de ejemplo. | Se aprobaron el contrato de entrada, los niveles, la matriz, el mínimo para Seguridad y la precedencia. El vocabulario y los textos de recomendaciones se aprobaron al autorizar la implementación. |
| Preparación de la integración | Estructuró la skill y el perfil según las referencias de VS Code y preparó casos de evaluación. | En esa fase se autorizaron seis archivos documentales y de configuración. La aprobación de la implementación llegó en la fase siguiente. |

## Implementación y validación automatizada

- Se verificó CPython 3.14.10 de 64 bits y se creó `.venv`. Se implementaron los cuatro endpoints y el servicio determinista con los catálogos y reglas aprobados. Se documentó la instalación local en PowerShell.
- La instalación en el entorno restringido no pudo resolver PyPI. La instalación autorizada fuera del sandbox completó FastAPI 0.165.0, Pydantic 2.14.4 y Uvicorn 0.54.0. En desarrollo se instalaron pytest 9.2.0, HTTPX 0.28.1 y PyYAML 6.0.4, además de las dependencias transitivas. `pip check` no detectó incompatibilidades.
- Las 29 pruebas del servicio pasaron dentro del sandbox. El diagnóstico de TestClient se detuvo en la creación del par de sockets locales de asyncio en Windows. La suite completa ejecutada fuera del sandbox obtuvo **55 pruebas aprobadas** (29 del servicio y 26 de HTTP y estructura de la skill). Starlette emitió un aviso de deprecación por su integración con HTTPX. Se mantuvieron las reglas aprobadas.
- Se verificó el YAML y la estructura de `SKILL.md` con pytest y el validador de Agent Skills disponible.

## Problemas de desarrollo y decisiones técnicas

| Problema observado | Resolución |
|---|---|
| Solicitudes desde PowerShell devolvían HTTP `400` al trabajar con caracteres especiales. Se reprodujo el fallo con un cuerpo declarado UTF-8 que contenía un byte ajeno a esa codificación. La codificación de las solicitudes originales no quedó registrada. | Se fijó UTF-8 explícito para el cuerpo HTTP y para decodificar la respuesta. La API publica en Swagger un formato común para `400` (cuerpo ilegible o JSON mal formado), `404` (ruta inexistente) y `422` (entrada que incumple el contrato). |
| En la sesión del estudiante, Windows PowerShell 5.1 tenía `Process: RemoteSigned`, los demás ámbitos informados estaban en `Undefined` y `pwsh` no estaba disponible. La política impidió ejecutar el archivo `.ps1`. El agente dejó el análisis pendiente. | La skill y el agente pasaron a invocar directamente el cliente Python de `.venv`. El adaptador `.ps1` quedó disponible para sesiones que permitan ejecutarlo. Las políticas del sistema se conservaron. |
| La tubería de PowerShell puede recodificar texto al pasarlo a un programa nativo. | El cliente usa la biblioteca estándar de Python. PowerShell transporta los bytes UTF-8 del POST como Base64 por la tubería. El cliente envía JSON UTF-8 sin BOM y devuelve `StatusCode` y `Body` en JSON con escapes Unicode. Se verificaron GET, POST con caracteres especiales y lectura de `422` desde PowerShell 5.1 y 7.6.9 contra la API local. |

## Pruebas manuales finales con Copilot

Resultados reportados por el estudiante tras implementar el cliente Python. Se utilizó el agente **Soporte IT** con la skill activa. Los nombres de los casos resumen las solicitudes. Las capturas correspondientes están incorporadas en `docs/evidencias/` y vinculadas al final de este documento. En dos intentos posteriores, el agente solicitó confirmación antes de analizar incidencias completas; al expresar explícitamente la intención de reportar una incidencia, se obtuvo la clasificación esperada.

| Caso | Resultado observado | Actividad de la API reportada |
|---|---|---|
| Incidencia de impresora | Hardware, prioridad Baja. | GET y POST con HTTP `200`. |
| Fallo general del sistema de facturación | Sistemas empresariales, prioridad Crítica. | GET y POST con HTTP `200`. |
| Correo sospechoso de phishing | Seguridad, prioridad Alta por la prioridad mínima de Seguridad. | GET y POST con HTTP `200`. |
| Información insuficiente | El agente solicitó aclaraciones. | Sin POST de análisis. |
| Consulta general sobre funciones en Python | El agente respondió a la consulta. | Sin consultas a la API. |
| API detenida | El agente informó que no podía conectarse y dejó el análisis pendiente, sin inventar categoría ni prioridad. | Conexión fallida. |

En las pruebas finales exitosas no se observaron HTTP `400` ni problemas de codificación. El estudiante también reportó pruebas manuales previas en Swagger con resultados funcionales correctos. El registro disponible no identifica los casos de Swagger uno por uno.

Los resultados informados cubren los seis casos de la tabla. El tratamiento manual de `422` por Copilot y los demás ejemplos del plan original quedan sin evidencia reportada. La suite automatizada sí cubre la respuesta HTTP `422`.

## Comparación con y sin la skill

| Condición | Resultado observado |
|---|---|
| Con la skill | En la prueba final reportada, el caso de la impresora devolvió Hardware, prioridad Baja, con GET y POST `200`. Una ejecución registrada mostró 5 pasos en 14 segundos. |
| Sin la skill | En una ejecución anterior, el agente resolvió el caso de la impresora, consultó más archivos, realizó solicitudes fallidas y tardó 73 segundos. |

Los tiempos de 73 y 14 segundos corresponden a ejecuciones individuales. La captura histórica sin skill muestra la consulta de archivos y la preparación de una solicitud, no el tiempo final; este último fue reportado por el estudiante. Además, entre los ensayos se modificó el cliente HTTP. Por ello, no se puede atribuir la diferencia exclusivamente a la skill ni generalizar una mejora de rendimiento.

## Reejecución automatizada

El 25 de noviembre de 2026 se ejecutó `pytest -q -o faulthandler_timeout=10` con el Python de `.venv`. Resultado: **59 pruebas aprobadas en 0.82 s**. Se mantuvo el aviso de Starlette por la deprecación de HTTPX con `TestClient`. La ejecución se hizo fuera del sandbox para permitir los sockets internos de asyncio en Windows.

La ejecución posterior del estudiante, respaldada por la captura 10, obtuvo **59 pruebas aprobadas, una advertencia y 1.48 s**.

## Evidencias incorporadas

Las diez capturas corresponden al 25 de noviembre de 2026. Las rutas son relativas a este documento.

| Captura | Evidencia observada |
|---|---|
| [01 — Swagger](evidencias/01-swagger.png) | Documentación de los cuatro endpoints; no muestra una solicitud ejecutada. |
| [02 — Skill detectada](evidencias/02-skill-detectada.png) | `analizar-ticket-it` aparece entre las habilidades disponibles de Copilot. Esto acredita su detección, no por sí solo su activación en cada consulta. |
| [03 — Impresora](evidencias/03-impresora-prioridad-baja.png) | Hardware, prioridad Baja. |
| [04 — Facturación](evidencias/04-facturacion-prioridad-critica.png) | Sistemas empresariales, prioridad Crítica. |
| [05 — Phishing](evidencias/05-phishing-prioridad-alta.png) | Seguridad, prioridad Alta por la regla de prioridad mínima. |
| [06 — Información insuficiente](evidencias/06-informacion-insuficiente.png) | Solicitud de aclaraciones antes de clasificar. |
| [07 — Consulta fuera de alcance](evidencias/07-consulta-fuera-de-alcance.png) | Respuesta a una consulta general de Python sin análisis de ticket. |
| [08 — API no disponible](evidencias/08-api-no-disponible.png) | Conexión rechazada; el agente deja el análisis pendiente. |
| [09 — Comparación sin skill](evidencias/09-comparacion-sin-skill.png) | Actividad histórica de lectura de archivos y preparación de una solicitud HTTP. |
| [10 — Pruebas automatizadas](evidencias/10-pruebas-automatizadas.png) | 59 pruebas aprobadas, una advertencia y 1.48 s. |

La versión exacta de VS Code y el modelo de todas las sesiones no quedaron registrados de forma uniforme. No se afirma una activación de la skill en cada sesión únicamente a partir de su disponibilidad. Las incidencias utilizadas son ficticias.
