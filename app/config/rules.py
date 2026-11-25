from app.models.tickets import (
    CategoryDefinition, LevelDefinition, MatrixEntry, PriorityCatalog,
    PriorityDefinition, SecurityException,
)

# El orden de esta tabla define la precedencia.
CATEGORY_RULES = (
    (
        CategoryDefinition(code="security", label="Seguridad", description="Actividad o contenido sospechoso."),
        ("phishing", "ransomware", "malware", "virus informático", "correo sospechoso", "acceso no autorizado"),
        ("Reportar al equipo de seguridad.", "Evitar interactuar con contenido sospechoso.", "Conservar las evidencias."),
    ),
    (
        CategoryDefinition(code="access", label="Accesos", description="Problemas de cuenta o permisos."),
        ("contraseña", "credenciales", "permisos", "cuenta bloqueada", "iniciar sesión"),
        ("Verificar el usuario.", "Comprobar el estado de la cuenta.", "Solicitar asistencia al administrador."),
    ),
    (
        CategoryDefinition(code="network", label="Redes", description="Problemas de conectividad."),
        ("internet", "Wi-Fi", "wifi", "VPN", "red", "conectividad"),
        ("Verificar la conexión física o inalámbrica.", "Comprobar si otros usuarios están afectados."),
    ),
    (
        CategoryDefinition(code="business_systems", label="Sistemas empresariales", description="Fallos de sistemas internos o de negocio."),
        ("ERP", "SAP", "facturación", "sistema interno"),
        ("Verificar la disponibilidad del sistema.", "Reportar al equipo responsable."),
    ),
    (
        CategoryDefinition(code="hardware", label="Hardware", description="Fallos de equipos o periféricos."),
        ("impresora", "teclado", "monitor", "mouse", "disco duro", "memoria RAM"),
        ("Comprobar las conexiones físicas.", "Registrar los síntomas del equipo."),
    ),
    (
        CategoryDefinition(code="software", label="Software", description="Fallos de aplicaciones o instalación."),
        ("Outlook", "Excel", "Word", "aplicación", "programa", "instalación de software"),
        ("Registrar el mensaje de error.", "Verificar si el problema es recurrente.", "Consultar al soporte técnico."),
    ),
    (
        CategoryDefinition(code="other", label="Otros", description="Incidencias sin coincidencias en el vocabulario."),
        (),
        ("Recopilar información adicional.", "Solicitar una revisión técnica."),
    ),
)

MATRIX = {
    ("low", "low"): "low",
    ("low", "medium"): "low",
    ("low", "high"): "medium",
    ("medium", "low"): "low",
    ("medium", "medium"): "medium",
    ("medium", "high"): "high",
    ("high", "low"): "medium",
    ("high", "medium"): "high",
    ("high", "high"): "critical",
}

PRIORITY_CATALOG = PriorityCatalog(
    impact_levels=[
        LevelDefinition(code="low", label="Bajo", description="Afecta a un usuario o equipo individual."),
        LevelDefinition(code="medium", label="Medio", description="Afecta a varios usuarios o a un departamento sin interrumpir un servicio crítico."),
        LevelDefinition(code="high", label="Alto", description="Afecta a toda la organización o interrumpe un servicio crítico."),
    ],
    urgency_levels=[
        LevelDefinition(code="low", label="Baja", description="El usuario puede continuar trabajando y la atención puede esperar."),
        LevelDefinition(code="medium", label="Media", description="El trabajo está limitado, pero existe una alternativa temporal."),
        LevelDefinition(code="high", label="Alta", description="El trabajo está detenido y requiere atención inmediata."),
    ],
    priority_levels=[
        PriorityDefinition(code="low", label="Baja", description="Atención ordinaria."),
        PriorityDefinition(code="medium", label="Media", description="Programar la atención según disponibilidad."),
        PriorityDefinition(code="high", label="Alta", description="Escalar al equipo responsable para atención prioritaria."),
        PriorityDefinition(code="critical", label="Crítica", description="Notificar inmediatamente al equipo responsable y activar el procedimiento de incidentes críticos, si existe."),
    ],
    matrix=[
        MatrixEntry(impact=impact, urgency=urgency, priority=priority)
        for (impact, urgency), priority in MATRIX.items()
    ],
    security_exception=SecurityException(category="security", minimum_priority="high"),
)
