# PLAN DE MIGRACIÓN Y SECUENCIA DE EJECUCIÓN (FASE E9)
## Transición hacia la Arquitectura Multiagente SIVAC-THESIS-LAB v3.0
> **Proyecto:** SIVAC-THESIS-LAB — Granja de Agentes de Investigación Científica  
> **Universidad:** Universidad Nacional José María Arguedas (UNAJMA) — EPIS  
> **Tesista / Autor:** Bach. José Luis Quispe León | **Asesora:** Dra. Norma Lorena Catacora Flores  
> **Fecha:** 2026-10-09  
> **Estado:** PLANIFICADO (A la espera de la palabra "APROBADO" para iniciar la Fase F)

---

## 1. Principios Rectores de la Migración

1. **Cero Pérdida de Datos:** Ningún archivo histórico o nota de Obsidian se elimina; todo elemento obsoleto se archiva en `_archive/`.
2. **Fuente Canónica Inviolable:** Todas las modificaciones se realizan exclusivamente en `.claude/`. El directorio `.factory/` es generado y reproducible.
3. **Puntos de Control y Reversibilidad:** Cada tarea cuenta con su procedimiento de verificación y su comando de reversión inmediata (`rollback`).
4. **Respaldo Previo Obligatorio:** Antes de tocar un solo archivo en la Fase F, se crea una rama de trabajo dedicada (`refactor/agent-farm-v3`) y un respaldo comprimido de seguridad.

---

## 2. Inventario de Bloques y Tareas de Migración

```
[BLOQUE 0: PREPARACIÓN Y SALVAGUARDA]
  ├── T0.1: Creación de rama Git `refactor/agent-farm-v3`
  └── T0.2: Respaldo de seguridad en `_archive/backup_pre_migracion_2026-10-09/`

[BLOQUE 1: PURIFICACIÓN Y AJUSTE DE LA FUENTE CANÓNICA (.claude/)]
  ├── T1.1: Limpieza de pseudo-skills en agentes (`context7` -> `mcpServers`)
  ├── T1.2: Ajuste de mínimo privilegio de herramientas (restringir `Execute`/shell a 4 agentes)
  ├── T1.3: Unificación de modelo operativo (`inherit` / `sonnet`)
  └── T1.4: Refinamiento de `AGENTS.md` como puente conciso hacia `CLAUDE.md`

[BLOQUE 2: CONSTRUCCIÓN DEL GENERADOR DE SINCRONIZACIÓN]
  ├── T2.1: Desarrollo del script canónico `scripts/sync_factory.py`
  ├── T2.2: Generación automática de `.factory/droids/*.md` con cabecera de advertencia
  ├── T2.3: Enlace directorio de `.factory/skills/` hacia `.claude/skills/`
  ├── T2.4: Generación de `.factory/mcp.json` con soporte de variables
  └── T2.5: Generación de `.factory/hooks.json` con códigos de salida compatibles (exit code 2)

[BLOQUE 3: CONSOLIDACIÓN DE OBSIDIAN Y REGLAS DE GOBERNANZA]
  ├── T3.1: Verificación de integridad de handoffs y bitácoras
  ├── T3.2: Actualización de `ESTADO_TESIS.md` reflejando el hito del ecosistema v3.0

[BLOQUE 4: PRUEBAS DE HUMO Y VERIFICACIÓN EN AMBAS CLIs]
  ├── T4.1: Prueba de humo en Factory Droid CLI (`/droids` y delegación vía `Task`)
  ├── T4.2: Prueba de humo en Claude Code CLI (`Agent(subagent_type)`)
  ├── T4.3: Prueba de sincronización bidireccional (modificar `.claude/` y re-sincronizar)
  └── T4.4: Documentación en `docs/CHANGELOG.md` y `docs/MANUAL_DE_USO.md`
```

---

## 3. Fichas Técnicas de Migración Tarea por Tarea

### TAREA 0.1 — Creación de Rama de Refactorización
- **Archivos Afectados:** Repositorio Git (`.git`).
- **Acción:** Ejecutar `git checkout -b refactor/agent-farm-v3`.
- **Riesgo:** Ninguno (operación local no destructiva).
- **Verificación:** `git branch --show-current` devuelve `refactor/agent-farm-v3`.
- **Reversión:** `git checkout master`.

---

### TAREA 1.1 — Limpieza de Pseudo-skills en Agentes
- **Archivos Afectados:**
  - `.claude/agents/ingeniero-sivac.md`
  - `.claude/agents/documentador-xp.md`
- **Acción:** Eliminar `context7` de la lista de `skills:` en el frontmatter YAML y ubicarlo en la sección descriptiva de servidores MCP.
- **Riesgo:** Bajo.
- **Verificación:** Ejecutar `python scripts/agentes/estado_granja.py` y comprobar que desaparece la advertencia de "skills que son MCP".
- **Reversión:** `git checkout -- .claude/agents/ingeniero-sivac.md .claude/agents/documentador-xp.md`.

---

### TAREA 1.2 — Aplicación del Principio de Mínimo Privilegio de Herramientas
- **Archivos Afectados:** `.claude/agents/*.md` (10 agentes revisores y redactores).
- **Acción:**
  - Retirar `Bash` y `PowerShell` de: `guardian-consistencia`, `especialista-instrumentos`, `especialista-forms`, `investigador-bibliografico`, `redactor-academico`, `curador-cerebro`, `jurado-revisor`.
  - Conservar `Bash` y `PowerShell` exclusivamente en: `director-general`, `maquetador-docx`, `analista-estadistico`, `analista-documental`, `verificador-integridad`.
- **Riesgo:** Medio (un agente analítico que requiera ejecutar un script deberá solicitarlo a través de un handoff o utilizar un agente de ejecución).
- **Verificación:** Inspección del frontmatter con script de verificación de herramientas.
- **Reversión:** `git checkout -- .claude/agents/`.

---

### TAREA 1.3 — Armonización de `AGENTS.md` y `CLAUDE.md`
- **Archivos Afectados:** `AGENTS.md` y `CLAUDE.md` en la raíz.
- **Acción:**
  - Mantener `CLAUDE.md` como la constitución maestra de principios innegociables (DEC-007, topología estrella, estilo APA 7).
  - Condensar `AGENTS.md` para que funcione como el mapa operativo y puente rápido que Droid lee al inicio, eliminando textos redundantes para optimizar el presupuesto de tokens (menos de 6,000 caracteres).
- **Riesgo:** Bajo.
- **Verificación:** Iniciar sesión en Droid y confirmar que el prompt del sistema no supera los límites de contexto.
- **Reversión:** `git checkout -- AGENTS.md CLAUDE.md`.

---

### TAREA 2.1 — Creación del Generador Determinista `scripts/sync_factory.py`
- **Archivos Afectados:** `scripts/sync_factory.py` (nuevo).
- **Acción:** Programar el script en Python que:
  1. Crea la estructura `.factory/` (`droids/`, `skills/`).
  2. Lee cada `.claude/agents/<agente>.md`, traduce las herramientas a nomenclatura Droid (`Write` $\to$ `Create`, `Bash/PowerShell` $\to$ `Execute`, etc.), ajusta `model: inherit`, inyecta la cabecera `<!-- GENERADO AUTOMÁTICAMENTE desde .claude/ — NO EDITAR DIRECTAMENTE -->` y escribe en `.factory/droids/<agente>.md`.
  3. Establece el enlace directorio o copia espejo de `.claude/skills/` hacia `.factory/skills/`.
  4. Lee `.mcp.json` y genera `.factory/mcp.json` con la ruta y variables correctas.
  5. Lee `.claude/settings.json` y genera `.factory/hooks.json` configurando los hooks `PreToolUse`, `SessionStart` y `SubagentStop` apuntando a `.claude/hooks/*.cjs`.
- **Riesgo:** Bajo.
- **Verificación:** Ejecutar `python scripts/sync_factory.py` y comprobar que todos los archivos se generan limpiamente en `.factory/`.
- **Reversión:** Eliminar `scripts/sync_factory.py` y la carpeta `.factory/`.

---

### TAREA 2.2 — Verificación de Validación en Droid (`DroidValidator`)
- **Archivos Afectados:** Archivos generados en `.factory/droids/`.
- **Acción:** Comprobar que Factory Droid reconoce los 14 agentes sin errores de validación mediante `droid mcp list` o inspección de subagentes.
- **Riesgo:** Ninguno.
- **Verificación:** Invocación de prueba de un subagente (`Task(subagent_type: "guardian-consistencia", ...)`).
- **Reversión:** Ajustar mapeo en `scripts/sync_factory.py` y re-ejecutar.

---

### TAREA 4.1 — Prueba de Humo de Extremo a Extremo
- **Archivos Afectados:** Ninguno (ejecución de prueba inocua).
- **Acción:**
  1. Comisionar a `guardian-consistencia` para verificar que la Matriz de Consistencia v3.0 mantiene las 3 dimensiones DEC-007.
  2. Comprobar que el subagente genera su nota de relevo en `08_SISTEMA_Y_AGENTES/handoffs/`.
  3. Comprobar que el hook `PreToolUse` bloquea intentos de escritura en rutas prohibidas.
- **Riesgo:** Ninguno.
- **Verificación:** Inspección de la nota generada y el log de ejecución.
- **Reversión:** Eliminar la nota de prueba.

---

## 4. Estado de Suspensión y Espera de Aprobación

Con la creación de este plan se concluyen formalmente las **Fases A, B, C, D y E**.  
En estricto cumplimiento de la **Regla Canónica 04** y del mandato expreso del Prompt Maestro v3:

⛔ **NO SE IMPLEMENTARÁ NINGÚN CAMBIO NI SE MODIFICARÁ NINGÚN ARCHIVO DEL SISTEMA HASTA QUE EL TESISTA ESCRIBA EXPLÍCITAMENTE "APROBADO".**
