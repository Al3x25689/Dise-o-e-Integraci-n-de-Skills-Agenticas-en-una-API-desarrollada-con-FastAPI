# Instrucciones del proyecto

IT Support API es un proyecto académico individual de Kodigo. La API concentra la clasificación, la prioridad, la justificación y las recomendaciones. Copilot recopila datos y presenta la respuesta de la API.

- Usa FastAPI y Pydantic. Separa rutas, modelos, configuración y servicios según [la arquitectura](ARCHITECTURE.md). Mantén las reglas en una sola configuración de ejecución y actualiza [su documentación](docs/REGLAS_NEGOCIO.md) cuando se aprueben cambios.
- Escribe la documentación en español y usa códigos de contrato estables. Usa únicamente incidencias ficticias, sin credenciales ni información empresarial real.
- Usa CPython instalado de 64 bits y compatible con las dependencias. Verifica versión y arquitectura antes de crear `.venv`. Ejecuta desde `.venv\Scripts\python.exe` e instala mediante `-m pip`. Mantén portables los lanzadores y excluye el entorno virtual del repositorio. Usa un intérprete de instalación normal, independiente de Codex.
- Mantén el alcance en los cuatro endpoints y la integración local. Quedan fuera persistencia, autenticación, frontend, Docker y servicios adicionales de IA.

## Criterios de terminado

Verifica los contratos en OpenAPI y ejecuta las pruebas unitarias y HTTP. Registra los resultados observados en [EVIDENCIAS_IA.md](docs/EVIDENCIAS_IA.md). Al documentar el flujo de Copilot, distingue las ejecuciones reportadas por el estudiante de las verificaciones automatizadas.
