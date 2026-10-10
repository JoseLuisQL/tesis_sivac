# REGISTRO DE CAMBIOS (CHANGELOG) — SIVAC-THESIS-LAB
> **Granja de Agentes de Investigación Científica para el Informe Final de Tesis**  
> **Escuela Profesional de Ingeniería de Sistemas — Universidad Nacional José María Arguedas (UNAJMA)**  
> **Proyecto:** APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II  
> **Tesista:** Bach. José Luis Quispe León | **Asesora:** Dra. Norma Lorena Catacora Flores  

Todas las modificaciones notables de esta infraestructura se documentan en este archivo bajo el estándar [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

---

## [3.0.0] — 2026-10-09
### Hito v3.0: Arquitectura Multiagente Dual (Claude Code + Factory Droid)

#### Resumen Ejecutivo
Esta versión consolida la madurez de la granja de agentes mediante una arquitectura multiplataforma simétrica y determinista. Permite operar indistintamente desde **Claude Code CLI** (Anthropic) o **Factory Droid CLI**, estableciendo la carpeta canónica `.claude/` como la **Única Fuente de Verdad (Single Source of Truth - SSOT)** y proyectando automáticamente la configuración hacia `.factory/` mediante el script determinista `scripts/sync_factory.py`.

---

#### 1. Estructura Canónica de 5 Capas Funcionales
Se formalizó la partición desacoplada del espacio de trabajo en cinco capas ortogonales:
- **Capa 0 (`.claude/`):** Motor de agentes, reglas modulares canónicas (`.claude/rules/`), hooks de ciclo de vida (`.claude/hooks/`), esquemas formales JSON (`.claude/schemas/`) y 21 skills operativas (`.claude/skills/`).
- **Capa 1 (`referencias/`):** Insumos inmutables de consulta protegidos contra escritura (modelos de tesis UNAJMA de Fany 2024 y Jhon 2026, modelos de validación del Dr. Cóndor Tinoco y `PROYECTO_TESIS.docx` original).
- **Capa 2 (`datos/`):** Pipeline de datos segregado en `raw/` (datos brutos inmutables una vez ingresados), `processed/` (datos limpios tabulados), `plantillas/` (formatos de campo en blanco) y `schemas/` (codebooks y diccionarios de variables).
- **Capa 3 (`scripts/`):** Herramientas de automatización divididas en `compiladores/` (maquetación capitular y maestro DOCX), `estadistica/` (inferencia R y Python), `figuras/` (generación de gráficos APA 7 a 300 DPI) y `utilidades/` (motor quirúrgico OpenXML).
- **Capa 4 (`salidas/`):** Entregables y artefactos generados categorizados en `documentos/` (informes finales versionados), `figuras/` (gráficos a 300 DPI), `instrumentos/` (expedientes de validación y fichas de campo) y `reportes_jurado/` (dictámenes simulados).

---

#### 2. Sincronizador Determinista Claude $\longrightarrow$ Factory Droid (`scripts/sync_factory.py`)
Se implementó un pipeline automatizado de sincronización unidireccional con validación de integridad (`--check` y `--force`):
- **Traducción Semántica de Herramientas (Tool Mapping):**
  - `Write` $\longrightarrow$ `Create`.
  - `Bash` y `PowerShell` $\longrightarrow$ `Execute` unificado.
  - `Agent` $\longrightarrow$ `Task` (confinado exclusivamente al Agente GOD `director-general`).
  - `AskUserQuestion` $\longrightarrow$ `AskUser`.
  - `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate` $\longrightarrow$ `TodoWrite`.
- **Sincronización de 14 Agentes Especializados (`.claude/agents/` $\longrightarrow$ `.factory/droids/`):**
  - Generación de los 14 droids correspondientes a los Squads A, B, C, D, E y F.
  - Mapeo de modelo a `model: inherit` para flexibilidad operativa.
  - Inserción de cabecera de advertencia de no edición manual (`<!-- GENERADO AUTOMÁTICAMENTE ... -->`).
- **Sincronización de 21 Skills Operativas (`.claude/skills/` $\longrightarrow$ `.factory/skills/`):**
  - Sincronización recursiva preservando descriptores `SKILL.md`, scripts de soporte y documentación.
- **Sincronización de Servidores MCP (`.mcp.json` $\longrightarrow$ `.factory/mcp.json`):**
  - Mapeo exacto de los 5 servidores configurados: `firecrawl`, `ydc-server`, `playwright`, `zotero` y `context7`.
- **Sincronización de Hooks de Ciclo de Vida (`.claude/settings.json` $\longrightarrow$ `.factory/settings.json`):**
  - Configuración de hooks: `PreToolUse`, `SessionStart`, `SubagentStop` y `Stop`.

---

#### 3. Mínimo Privilegio y Blindaje de Seguridad
- **Protección de Código Fuente del Sistema (`syncova`):** Bloqueo categórico de escritura sobre el directorio de desarrollo del software SIVAC (`C:\Proyectos\syncova`). El hook `PreToolUse` intercepta cualquier intento de modificación, limitando el rol del `ingeniero-sivac` y demás agentes a estricta lectura e inspección arquitectónica.
- **Inmutabilidad de Insumos Base:** Blindaje de solo lectura sobre `referencias/` para preservar intactos los modelos oficiales institucionales y el documento de proyecto original.
- **Preservación del Cerebro Digital (Obsidian):** Prohibición expresa de operaciones destructivas o sobreescrituras descontroladas en `C:\MisInvestigaciones\obsidian_vault`. El `curador-cerebro` actúa como custodio del historial vivo.
- **Erradicación de Scripts Ad-Hoc:** Prohibición de proliferación de scripts temporales `vX_Y.py`; consolidación obligatoria de utilidades en el motor central `scripts/utilidades/docx_quirurgico.py`.

---

#### 4. Consistencia Metodológica y Retrocompatibilidad
- **Blindaje de DEC-007:** Ratificación inmutable de las 3 dimensiones oficiales de la Variable Dependiente (*Oportunidad de procesamiento*, *Consistencia documental*, *Satisfacción del usuario bajo TAM*).
- **Compatibilidad con Versiones Previas:**
  - Plena compatibilidad con artefactos compilados en la versión v1.0 (`PROYECTO_TESIS.docx`) y v2.0 (`PROYECTO_TESIS_ACTUALIZADO_V2.docx`, `V3_NORMALIZADO`, `V4_NORMALIZADO`).
  - Total interoperabilidad con el Informe Final Pre-Campo (`informe_final_v01.docx`) y el expediente de validación psicométrica por juicio de expertos.

---

## [2.1.0] — 2026-10-08
### Consolidación Pre-Campo del Informe Final y Expediente de Validación
- Compilación del Informe Final de Tesis v01 (`informe_final_v01.docx`) con estructura 1:1 de los modelos UNAJMA (`Jhon 2026` y `Fany 2024`).
- Integración de 18 tablas nativas APA 7, 19 figuras oficiales a 300 DPI y 12 fórmulas OMML nativas.
- Erradicación del 100% de ocurrencias del guion largo (`U+2014`) en prosa e índices.
- Compilación del paquete completo de instrumentos y expediente de validación por expertos de la EPIS-UNAJMA (Fichas 01 y 02, Cuestionario TAM 03, expediente en Word y matriz Excel de IVC / V de Aiken).

---

## [2.0.0] — 2026-10-02
### Reestructuración Metodológica Quirúrgica y Normalización Editorial
- Adopción vinculante de la Decisión DEC-007: 3 dimensiones inmutables de la VD.
- Desacoplamiento de la Variable Independiente como intervención tecnológica manipulada experimentalmente ($X_0$ manual vs. $X_1$ SIVAC).
- Definición de población censal $N = n = 14$ en diseño preexperimental ($O_1 \longrightarrow X \longrightarrow O_2$).
- Creación de fórmulas centradas OMML para indicadores $T_{reg}$, $T_{vale}$, $RSD$ y $CPE$.
- Corrección de la fórmula de $CPE$ a proporción acotada en $[0, 100]\%$.

---

## [1.0.0] — 2026-09-30
### Nacimiento del Ecosistema SIVAC-THESIS-LAB
- Inicialización de la granja de agentes y constitución operativa `CLAUDE.md`.
- Desglose inicial de `PROYECTO_TESIS.docx` (588 párrafos, 12 tablas).
- Configuración de la bóveda de Obsidian (`00_SISTEMA` a `09_CANVAS_Y_DIAGRAMAS`).
- Configuración de la colección de Zotero con 26 fuentes primarias iniciales y vinculación a PDFs locales.
