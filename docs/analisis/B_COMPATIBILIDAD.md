# INFORME DE VERIFICACIÓN DE COMPATIBILIDAD `.claude/` ↔ DROID (FASE B)
> **Proyecto:** SIVAC-THESIS-LAB — Granja de Agentes de Investigación Científica  
> **Versiones de Entorno Verificadas:**  
> - **Factory Droid CLI:** `0.237.0`  
> - **Claude Code:** `2.1.295`  
> - **Sistema Operativo:** Windows 11 Pro (win32 10.0.26200), PowerShell 7+  
> **Fecha de Evaluación:** 2026-10-09  
> **Arquitecto Evaluador:** Arquitecto Senior de Sistemas Multiagente Autónomos  

---

## 1. Resultados Empíricos y Documentales de las Pruebas B1 a B10

| # | Prueba de Compatibilidad | Mecanismo de Verificación | Resultado Empírico / Documental | Veredicto |
|---|---|---|---|---|
| **B1** | **¿Droid lee `CLAUDE.md`?** | Inspección del contexto de arranque de Droid y especificación oficial de nombres compatibles en `https://docs.factory.com/harness/agents-md.md`. | **SÍ.** Droid reconoce nativamente `CLAUDE.md` (y su variante `Claude.md`) como archivo de instrucciones de proyecto compatible. En la sesión activa, Droid inyectó el contenido de `CLAUDE.md` directamente en el prompt del sistema (`# Project Instructions:`). | **COMPATIBLE (NATIVO)** |
| **B2** | **¿Prioridad `AGENTS.md` vs `CLAUDE.md`?** | Verificación de carga en sesión con ambos archivos presentes en la raíz. | **CONCATENACIÓN / CONFLICTO DE PRESUPUESTO.** Droid carga ambos archivos en el contexto inicial hasta un límite conjunto de 80,000 caracteres. Si ambos existen, compiten por el presupuesto de tokens y pueden duplicar directivas. La regla oficial de Droid prescribe usar `AGENTS.md` como nombre primario y dejar `CLAUDE.md` como compatibilidad. | **REQUIERE PUENTE UNIFICADO** |
| **B3** | **¿Droid detecta `.claude/agents/` sin importar?** | Inspección de discovery en CLI Droid y lectura de `https://docs.factory.com/harness/subagents.md`. | **NO.** Droid solo escanea `.factory/droids/` (a nivel de proyecto) y `~/.factory/droids/` (a nivel de usuario). Los agentes en `.claude/agents/` son completamente invisibles para el comando `/droids` y la herramienta `Task(subagent_type)` si no están en `.factory/droids/`. | **INCOMPATIBLE SIN CAPA ADAPTADORA** |
| **B4** | **Importación oficial de agentes vía Droid UI** | Análisis del flujo de importación documentado en `/droids` ("Import from Claude Code"). | **PARCIAL Y MANUAL.** Droid provee un asistente interactivo en la TUI que lee `/.claude/agents/`, convierte nombres de herramientas y modelos, y escribe en `.factory/droids/`. Sin embargo, es un proceso manual por menús que no se puede ejecutar en scripts automatizados ni garantiza sincronización continua tras editar `.claude/`. | **INSUFICIENTE PARA CI/AUTOMATIZACIÓN** |
| **B5** | **Symlink / Junction directo de agentes (`.factory/droids → .claude/agents`)** | Prueba de enlaces en Windows (`mklink /J`) y análisis del validador de esquemas `DroidValidator`. | **FALLA EN VALIDACIÓN DE HERRAMIENTAS.** Aunque la creación de un Directory Junction (`mklink /J`) es 100% soportada en Windows sin permisos de administrador, el validador de Droid (`DroidValidator`) rechaza los archivos `.md` de `.claude/agents/` debido a que contienen nombres de herramientas de Claude Code (`Bash`, `PowerShell`, `Write`, `Agent`, `TaskCreate`, `AskUserQuestion`). Droid exige herramientas con nombres exactos (`Execute`, `Create`, `Task`, `AskUser`, `TodoWrite`). | **NO VIABLE COMO ENLACE DIRECTO** |
| **B6** | **Skills: compatibilidad e importación (`.claude/skills` vs `.factory/skills`)** | Comparación estructural de archivos `SKILL.md` y verificación de directorios compatibles. | **100% COMPATIBLE MEDIANTE SYMLINK / JUNCTION.** Tanto Claude Code como Droid emplean el estándar de carpeta con `SKILL.md`, `name` y `description` en YAML frontmatter, y soporte de archivos auxiliares (`checklists`, `scripts`, `references`). Droid busca en `.factory/skills/`, `.agents/skills/` o carpetas de misión. Un junction o copia directa funciona sin modificación de contenido. | **COMPATIBLE (ESTÁNDAR ABIERTO)** |
| **B7** | **MCP: Formato y ubicación de configuración** | Inspección de `.mcp.json` vs `.factory/mcp.json` y `~/.factory/mcp.json`. | **DIVERGENCIA DE UBICACIÓN.** Claude Code lee `.mcp.json` en la raíz del proyecto. Factory Droid requiere que esté en `.factory/mcp.json` (proyecto) o `~/.factory/mcp.json` (usuario). Ambos admiten la sintaxis de variables `${VAR}` en encabezados HTTP y entornos stdio. | **REQUIERE GENERACIÓN DE `.factory/mcp.json`** |
| **B8** | **Hooks: Eventos, payload y códigos de salida** | Comparación de `.claude/settings.json` vs `.factory/hooks.json` (doc oficial). | **SINTAXIS ANÁLOGA CON DIFERENCIA EN EXIT CODES.** Ambos sistemas pasan JSON por `stdin` con `tool_name` y `tool_input`. Claude bloquea con salida distinta de 0; Droid utiliza específicamente `exit code 2` para bloqueo correctivo y `exit code 0` para éxito. Los mismos scripts Node.js (`.claude/hooks/*.cjs`) pueden ser reutilizados con una mínima verificación del código de retorno. | **COMPATIBLE CON CONFIGURACIÓN GENERADA** |
| **B9** | **Herramientas: Nombres nativos en cada CLI** | Mapeo 1:1 entre los catálogos de herramientas de Claude Code y Factory Droid. | **MAPEO DETERMINISTA EXISTENTE.** Existe una traducción biunívoca exacta: `Write` $\to$ `Create`, `Bash/PowerShell` $\to$ `Execute`, `Agent` $\to$ `Task`, `AskUserQuestion` $\to$ `AskUser`, `TaskCreate/TaskList` $\to$ `TodoWrite`. | **CONVERTIBLE AUTOMÁTICAMENTE** |
| **B10** | **Invocación de subagentes (Delegación de GOD)** | Mecanismo de invocación de subagentes en Claude Code vs Factory Droid. | **SINTAXIS DIFERENTE, SEMÁNTICA EQUIVALENTE.** En Claude Code: `Agent(subagent_type: "nombre", prompt: "...")`. En Droid: `Task(subagent_type: "nombre", description: "...", prompt: "...", await: true)`. La orquestación en estrella radial se mantiene idéntica. | **EQUIVALENTE FUNCIONAL** |

---

## 2. Evaluación y Selección de la Estrategia de Sincronización

Se evaluaron formalmente las 3 opciones requeridas por el mandato de arquitectura:

### Evaluación Comparativa

```
Estrategia 1: Symlinks Puros (Junctions Windows)
  [X] Falla: DroidValidator rechaza las herramientas de Claude Code (Bash, Write, Agent) en los agentes.
  [X] Falla: Droid no lee .mcp.json en la raíz ni .claude/settings.json para hooks.

Estrategia 2: Importación Manual Oficial (/droids)
  [X] Falla: Requiere interacción humana en la TUI en cada cambio.
  [X] Falla: No es reproducible, no admite versionado ni se integra en scripts de compilación.

Estrategia 3: Generador Determinista Automático (`scripts/sync_factory.py`)
  [V] Éxito: Mantiene `.claude/` como la ÚNICA fuente de verdad absoluta.
  [V] Éxito: Transforma quirúrgicamente el frontmatter de los 14 agentes para que pasen DroidValidator.
  [V] Éxito: Enlaza o copia las 21 skills sin alterar su contenido canónico.
  [V] Éxito: Genera `.factory/mcp.json` y `.factory/hooks.json` reutilizando los mismos scripts .cjs.
  [V] Éxito: Inyecta en cada archivo generado la cabecera:
             <!-- GENERADO desde .claude/ — NO EDITAR DIRECTAMENTE -->
```

---

## 3. Dictamen y Recomendación de Arquitectura

**SE SELECCIONA LA OPCIÓN 3: SCRIPT DETERMINISTA `scripts/sync_factory.py`.**

### Justificación Técnica:
1. **Inviolabilidad de la Fuente de Verdad:** El usuario y los agentes solo editan archivos dentro de `.claude/`. El directorio `.factory/` pasa a ser un artefacto de compilación efímero y 100% reproducible.
2. **Cero Fricción en Windows:** Evita inconsistencias de enlaces simbólicos entre sistemas de archivos y permisos de usuario.
3. **Mapeo Limpio de Herramientas:** Corrige el problema de validación de `DroidValidator`, garantizando que tanto Claude Code como Factory Droid ejecuten los mismos 14 agentes con sus permisos nativos correctos.
4. **Idempotencia:** El script se podrá ejecutar en cualquier momento (`python scripts/sync_factory.py`) o conectarse a un hook de sesión para que `.factory/` esté perpetuamente sincronizado con `.claude/`.
