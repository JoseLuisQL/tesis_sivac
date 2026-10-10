# MANUAL MAESTRO DE EQUIVALENCIAS DE PLATAFORMA
## Claude Code CLI (v2.1+) $\longleftrightarrow$ Factory Droid CLI (v0.237+)
> **SIVAC-THESIS-LAB — Escuela Profesional de Ingeniería de Sistemas (UNAJMA)**  
> **Documento Canónico de Arquitectura y Adaptación Multiplataforma**  
> **Fecha de Emisión:** 2026-10-09  
> **Principio Rector:** `.claude/` es la única fuente de verdad; `.factory/` es una capa generada y adaptada.

---

## 1. Tabla Maestra de Mapeo de Herramientas (Tools)

En Claude Code y Factory Droid, los nombres de las herramientas operativas difieren en nomenclatura pero comparten semántica. El generador `sync_factory.py` aplica la siguiente matriz de traducción en el campo `tools` del frontmatter:

| Capacidad Operativa | Herramienta en Claude Code | Herramienta en Factory Droid | Regla de Adaptación / Restricción |
|---|---|---|---|
| **Lectura de archivos** | `Read` | `Read` | Idéntica. En Droid requiere rutas absolutas o relativas válidas. |
| **Edición parcial de texto** | `Edit` | `Edit` | Idéntica. Coincidencia exacta de cadenas con `old_str` y `new_str`. |
| **Creación/Sobrescritura** | `Write` | `Create` | **Traducción obligatoria:** `Write` $\to$ `Create`. |
| **Búsqueda por contenido** | `Grep` | `Grep` | Idéntica. Envoltura de ripgrep. |
| **Búsqueda por nombre/patrón** | `Glob` | `Glob` | Idéntica. Soporta globs y exclusiones. |
| **Listado de directorios** | `LS` (o `Bash ls`) | `LS` | Idéntica. |
| **Ejecución en terminal** | `Bash`, `PowerShell` | `Execute` | **Traducción obligatoria:** Tanto `Bash` como `PowerShell` se mapean a `Execute`. En Windows, Droid ejecuta en PowerShell 7. |
| **Delegación en subagente** | `Agent` | `Task` | **Traducción obligatoria:** `Agent` $\to$ `Task`. Solo autorizada en `director-general`. |
| **Consulta interactiva** | `AskUserQuestion` | `AskUser` | **Traducción obligatoria:** `AskUserQuestion` $\to$ `AskUser`. Deshabilitada dentro de subagentes. |
| **Invocación de habilidades** | `Skill` | `Skill` | Idéntica. Invoca carpetas con `SKILL.md`. |
| **Gestión de tareas (Todos)** | `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate` | `TodoWrite` | **Traducción obligatoria:** Se consolida en `TodoWrite`. |
| **Búsqueda Web** | `WebSearch` | `WebSearch` | Disponible como herramienta diferida en Droid. |
| **Descarga de URLs** | `FetchUrl` | `FetchUrl` | Disponible como herramienta diferida en Droid. |

---

## 2. Frontmatter de Agentes (`.claude/agents/*.md` $\to$ `.factory/droids/*.md`)

### 2.1. Matriz de Campos y Transformaciones

| Campo YAML | En Claude Code (`.claude/agents/`) | En Factory Droid (`.factory/droids/`) | Transformación Aplicada |
|---|---|---|---|
| `name` | Requerido (`nombre-agente`) | Requerido (`nombre-agente`) | Copia directa (debe coincidir con el nombre de archivo). |
| `description` | Resumen para invocación del modelo | Resumen mostrado en `/droids` y Task | Copia directa (máximo 500 caracteres para evitar advertencias). |
| `model` | `opus`, `sonnet`, `haiku`, o display name | `inherit` o ID público de modelo (`claude-sonnet-4-5-...`) | En Droid se recomienda `inherit` para adoptar el modelo de la sesión, o mapear `sonnet` $\to$ `claude-sonnet-4-5-20250929` y `opus` $\to$ `claude-opus-4-20250514`. |
| `tools` | Array de herramientas Claude (`Read`, `Write`, `Bash`, etc.) | Array de herramientas Droid (`Read`, `Create`, `Execute`, etc.) | **Traducción 1:1** según la tabla de la Sección 1. Se eliminan duplicados (`Bash` + `PowerShell` $\to$ un solo `Execute`). |
| `skills` | Lista de skills declaradas | Campo no nativo en Droid (Droid inyecta `Skill` automáticamente) | Se preserva en el cuerpo del prompt como guía directiva o se mapea a instrucciones del sistema. |
| `squad` / `role` | Metadatos organizativos | Metadatos no estándar en Droid | Se preservan en el cuerpo del markdown como contexto de rol. |
| `mcpServers` | N/A (hereda del entorno global) | Array opcional de nombres de servidores MCP | Permite acotar qué MCPs ve el subagente (ej. `["zotero"]`). |

### 2.2. Ejemplo Canónico de Transformación

**Fuente en `.claude/agents/verificador-integridad.md`:**
```yaml
---
name: verificador-integridad
description: Auditor implacable de integridad académica y anti-alucinaciones...
model: sonnet
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - PowerShell
skills:
  - zotero-busqueda-academica
  - academic-paper
squad: Squad A (Inteligencia Bibliográfica y Evidencia)
role: Auditor de Integridad Académica
---
```

**Generado en `.factory/droids/verificador-integridad.md`:**
```yaml
---
# <!-- GENERADO AUTOMÁTICAMENTE desde .claude/agents/ — NO EDITAR DIRECTAMENTE -->
name: verificador-integridad
description: Auditor implacable de integridad académica y anti-alucinaciones...
model: inherit
tools:
  - Read
  - Create
  - Edit
  - Grep
  - Glob
  - Execute
mcpServers:
  - zotero
---
```

---

## 3. Skills (`.claude/skills/` $\longleftrightarrow$ `.factory/skills/`)

### 3.1. Estructura y Compatibilidad
Ambas plataformas adhieren al estándar **Agent Skills**:
- Entrada obligatoria: archivo `SKILL.md` dentro de una subcarpeta con el nombre de la skill.
- Metadatos YAML frontmatter:
  ```yaml
  ---
  name: matriz-consistencia
  description: Metodología y reglas de consistencia interna para la tesis SIVAC...
  user-invocable: true
  disable-model-invocation: false
  ---
  ```
- Soporte de archivos secundarios: `scripts/`, `templates/`, `references/` ubicados al lado de `SKILL.md`.

### 3.2. Estrategia de Acceso
Dado que la sintaxis y los archivos de apoyo son 100% idénticos, `.factory/skills/` se sincroniza como enlace directorio (Junction en Windows) o copia directa desde `.claude/skills/` sin necesidad de alterar ningún byte de los manuales de skill.

---

## 4. Servidores MCP (`.mcp.json` $\longleftrightarrow$ `.factory/mcp.json`)

### 4.1. Ubicación y Precedencia
- **Claude Code:** Lee exclusivamente `.mcp.json` en la raíz del proyecto.
- **Factory Droid:** Lee en tres niveles:
  1. Proyecto: `.factory/mcp.json` (dentro de la carpeta `.factory/`).
  2. Usuario: `~/.factory/mcp.json`.
  3. Carpeta superior: `.factory/mcp.json`.

### 4.2. Estructura del Documento
Ambos comparten la clave raíz `"mcpServers"`.
- Soporte de transporte: `stdio`, `http` (streamable HTTP/SSE) y `sse`.
- Expansión de variables de entorno: `${VARIABLE}` es soportada por ambas plataformas para no almacenar tokens o API keys en texto plano en el repositorio.

---

## 5. Ciclo de Vida de Hooks y Payloads

### 5.1. Matriz de Eventos Compatibles

| Evento de Ciclo de Vida | Claude Code (`.claude/settings.json`) | Factory Droid (`.factory/hooks.json`) | Compatibilidad / Comportamiento |
|---|---|---|---|
| **Antes de ejecutar herramienta** | `PreToolUse` | `PreToolUse` | **100% idéntico.** Recibe `{ tool_name, tool_input }`. |
| **Después de ejecutar herramienta** | `PostToolUse` | `PostToolUse` | Recibe `{ tool_name, tool_input, tool_response }`. |
| **Inicio de sesión** | `SessionStart` | `SessionStart` | Inyecta contexto de arranque o imprime estado de tesis. |
| **Fin de subagente** | `SubagentStop` | `SubagentStop` | Emite recordatorio de handoff para Obsidian. |
| **Fin de sesión principal** | `Stop` | `Stop` | Valida cierre de tarea. |

### 5.2. Códigos de Salida y Mecanismos de Bloqueo
- **Claude Code:**
  - Código `0`: Éxito.
  - Código distinto de `0`: Bloqueo con mensaje en `stderr`.
- **Factory Droid:**
  - Código `0`: Éxito / Permitir.
  - Código `2`: **Bloqueo correctivo.** Bloquea la acción y retroalimenta `stderr` al agente para que rectifique.
  - JSON en stdout: Soporta `{ "hookSpecificOutput": { "permissionDecision": "deny", "permissionDecisionReason": "..." } }`.

---

## 6. Protocolo de Invocación y Delegación de Subagentes

### En Claude Code (Sesión Principal del Director General):
```javascript
Agent({
  subagent_type: "verificador-integridad",
  prompt: `
TAREA: Auditar correspondencia de citas en Capítulo IV
FASE: F9
SQUAD: Squad A
SUBAGENTE: verificador-integridad
ENTRADAS: salidas/documentos/informe_final_v01.docx
SALIDA ESPERADA: Informe de auditoría con lista de citas y DOIs
RESTRICCIONES: Regla 01 (Cero alucinaciones)
CRITERIO DE ÉXITO: 0 citas huérfanas
`
});
```

### En Factory Droid (Sesión Principal del Director General):
```javascript
Task({
  subagent_type: "verificador-integridad",
  description: "Auditar citas Cap IV",
  prompt: `
TAREA: Auditar correspondencia de citas en Capítulo IV
FASE: F9
SQUAD: Squad A
SUBAGENTE: verificador-integridad
ENTRADAS: salidas/documentos/informe_final_v01.docx
SALIDA ESPERADA: Informe de auditoría con lista de citas y DOIs
RESTRICCIONES: Regla 01 (Cero alucinaciones)
CRITERIO DE ÉXITO: 0 citas huérfanas
`,
  await: true
});
```

### Reglas Inviolables de Delegación:
1. **Los subagentes no delegan:** En ambas plataformas, la herramienta de subagentes (`Agent` o `Task`) está prohibida dentro de los subagentes ejecutados.
2. **Handoff persistente:** Al terminar, el subagente deposita su resultado en:
   `C:\MisInvestigaciones\obsidian_vault\08_SISTEMA_Y_AGENTES\handoffs\AAAA-MM-DD_<agente>_<tarea>.md`
3. **El Director no ejecuta en solitario:** El Director General planifica, delega y valida, pero no escribe capítulos ni compila documentos sin la intervención de sus especialistas.
