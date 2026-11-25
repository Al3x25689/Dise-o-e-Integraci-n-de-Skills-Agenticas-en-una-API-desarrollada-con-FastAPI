# Reglas de negocio

## Entrada aprobada

El análisis exige `description` de tipo texto y longitud de 5 a 2000 caracteres después de quitar espacios de los extremos. `impact` y `urgency` admiten los códigos exactos `low`, `medium` y `high`. Los campos faltantes, desconocidos o inválidos generan HTTP `422` con el [formato de errores de la API](../ARCHITECTURE.md#contratos-aprobados-para-el-diseño). El análisis requiere los tres campos.

| Código | Impacto | Urgencia |
|---|---|---|
| `low` | Afecta a un usuario o equipo individual. | El usuario puede continuar trabajando y la atención puede esperar. |
| `medium` | Afecta a varios usuarios o a un departamento sin interrumpir un servicio crítico. | El trabajo está limitado, pero existe una alternativa temporal. |
| `high` | Afecta a toda la organización o interrumpe un servicio crítico. | El trabajo está detenido y requiere atención inmediata. |

## Matriz aprobada

| Impacto / Urgencia | `low` | `medium` | `high` |
|---|---|---|---|
| `low` | `low` | `low` | `medium` |
| `medium` | `low` | `medium` | `high` |
| `high` | `medium` | `high` | `critical` |

Los códigos corresponden a Baja, Media, Alta y Crítica. Si la categoría es `security`, elevar a `high` cuando la matriz indique `low` o `medium`. Conservar `high` o `critical` si la matriz ya los indica. Todas las respuestas de prioridad Alta o Crítica incluyen escalamiento.

## Clasificación y recomendaciones aprobadas

Comparar términos y frases sin distinguir mayúsculas ni acentos, respetando los límites de palabra. Aplicar el orden de la tabla y usar la primera categoría con coincidencias. Usar `other` si no hay coincidencias.

| Categoría | Vocabulario | Recomendaciones |
|---|---|---|
| `security` · Seguridad | phishing, ransomware, malware, virus informático, correo sospechoso, acceso no autorizado | Reportar al equipo de seguridad, evitar interactuar con contenido sospechoso y conservar evidencias. |
| `access` · Accesos | contraseña, credenciales, permisos, cuenta bloqueada, iniciar sesión | Verificar el usuario, comprobar el estado de la cuenta y solicitar asistencia al administrador. |
| `network` · Redes | internet, Wi-Fi, wifi, VPN, red, conectividad | Verificar la conexión física o inalámbrica y comprobar si otros usuarios están afectados. |
| `business_systems` · Sistemas empresariales | ERP, SAP, facturación, sistema interno | Verificar la disponibilidad del sistema y reportar al equipo responsable. |
| `hardware` · Hardware | impresora, teclado, monitor, mouse, disco duro, memoria RAM | Comprobar conexiones físicas y registrar los síntomas. |
| `software` · Software | Outlook, Excel, Word, aplicación, programa, instalación de software | Registrar el error, verificar si es recurrente y consultar a soporte técnico. |
| `other` · Otros | Sin coincidencias | Recopilar información adicional y solicitar una revisión técnica. |

La versión inicial evalúa coincidencias textuales. Una negación como «No hay malware» activa Seguridad. La precedencia puede favorecer una mención secundaria frente a la causa real. Las variantes de escritura fuera del vocabulario pueden quedar en Otros.

## Atención por prioridad

| Prioridad | Acción |
|---|---|
| `low` | Atención ordinaria. |
| `medium` | Programar atención según disponibilidad. |
| `high` | Escalar al equipo responsable para atención prioritaria. |
| `critical` | Notificar inmediatamente al equipo responsable y activar el procedimiento de incidentes críticos, si existe. |

La respuesta agrega la acción de prioridad después de las recomendaciones de categoría. La API carece de tiempos de SLA. Las recomendaciones deben evitar acciones destructivas, desactivar herramientas de seguridad y solicitar contraseñas.

## Casos de referencia

| Entrada ficticia | Resultado esperado |
|---|---|
| Impresora con cada par de impacto y urgencia | Las nueve prioridades de la matriz. |
| «Detecté PHÍSHING y una cuenta bloqueada» con `low` / `low` | `security`, `high` y escalamiento. |
| «Alerta de malware» con `high` / `high` | `security`, `critical` y escalamiento. |
| «Cuenta bloqueada en el ERP» con `medium` / `medium` | `access` y `medium`. |
| «El supermonitor vibra» | `other` por límites de palabra. |
| «No hay malware, solo falla el monitor» | `security` por coincidencia literal y precedencia. |
| Descripciones de 5 o 2000 caracteres tras recorte | Aceptadas con los demás campos válidos. |
| Campo desconocido, ausente, con valor inválido o de tipo incorrecto | `422`. |
