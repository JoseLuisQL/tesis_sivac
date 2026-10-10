# INFORME DE RECONOCIMIENTO TOTAL DEL SISTEMA (FASE A)
> **Proyecto:** SIVAC-THESIS-LAB — Granja de Agentes de Investigación Científica  
> **Tesis:** Aplicación del sistema SIVAC para mejorar la gestión de movimientos de vacunas en la DISA Apurímac II  
> **Universidad:** Universidad Nacional José María Arguedas (UNAJMA) — EPIS  
> **Autor / Tesista:** Bach. José Luis Quispe León | **Asesora:** Dra. Norma Lorena Catacora Flores  
> **Fecha de Reconocimiento:** 2026-10-09  
> **Arquitecto Evaluador:** Arquitecto Senior de Sistemas Multiagente Autónomos  
> **Modo Operativo:** FASE A (Solo Lectura y Análisis Estructural)

---

## 1. Resumen Ejecutivo de la Fase A

El ecosistema **SIVAC-THESIS-LAB** es una granja multiagente madura, funcional y altamente especializada, concebida originalmente bajo las especificaciones de **Claude Code** y operando sobre una topología radial jerárquica **Hub-and-Spoke (Estrella)**. El sistema ya ha superado con éxito las fases de diagnóstico documental, armonización metodológica de la variable dependiente (fijada en 3 dimensiones oficiales bajo DEC-007) y consolidación editorial del borrador de tesis hasta la versión `informe_final_v01.docx`.

No obstante, el análisis estructural revela fricciones arquitectónicas de interoperabilidad y gobierno:
1. **Asimetría de plataformas:** Todo el núcleo reside en `.claude/` y `.mcp.json`. No existe actualmente un directorio `.factory/` en el proyecto ni definición de custom droids en `~/.factory/droids/` para los 14 agentes de tesis. Factory Droid consume el sistema a través de un puente híbrido donde el orquestador principal ejecuta scripts y delega tareas como un trabajador genérico, en lugar de disponer de agentes declarativos nativos.
2. **Discrepancias de metadatos:** Existen divergencias en los modelos declarados entre `AGENTS.md` (que lista `opus` para todos los especialistas) y los archivos `.claude/agents/*.md` (que declaran `sonnet`). Asimismo, herramientas de ejecución shell (`Bash`, `PowerShell`) están asignadas a 12 de los 14 agentes, violando el principio de mínimo privilegio.
3. **Cerebro persistente robusto pero monolítico:** El vault de Obsidian (`C:\MisInvestigaciones\obsidian_vault`) almacena 42 notas de handoff y un registro pormenorizado en `00_SISTEMA/ESTADO_TESIS.md`, funcionando con éxito como memoria viva pero dependiendo del sistema de archivos local sin comprobación de sintaxis o metadatos automatizada por hooks en Droid.
4. **Pipeline DOCX de alta precisión:** La compilación de Word no usa generadores Markdown genéricos tipo Pandoc, sino un ensamblador OpenXML directo (`scripts/compiladores/` y `scripts/utilidades/docx_quirurgico.py`) que inyecta ecuaciones matemáticas nativas `<m:oMath>`, tablas APA 7 y figuras a 300 DPI.

---

## 2. A1. Inventario Exhaustivo del Sistema y Entorno

### 2.1. Nivel de Proyecto (`C:\MisInvestigaciones\tesis\sivac\`)
- **Archivos Raíz Canónicos:**
  - `CLAUDE.md`: Constitución operativa (8,049 bytes). Define las 3 dimensiones DEC-007, la topología estrella y las 4 reglas canónicas.
  - `AGENTS.md`: Matriz de squads, catálogo de 14 agentes, contratos de comisión/handoff y compuertas QG-0 a QG-9 (11,223 bytes).
  - `.mcp.json`: Servidores MCP configurados para Claude Code (`firecrawl`, `ydc-server`, `playwright`).
  - `.gitignore`: Exclusiones de seguridad (entorno virtual, temporales, backups).
  - `requirements.txt`: Dependencias científicas y editoriales de Python.
- **Directorio `.claude/` (Fuente Canónica):**
  - `.claude/agents/`: 14 archivos Markdown de agentes (`analista-documental.md`, `analista-estadistico.md`, `curador-cerebro.md`, `director-general.md`, `documentador-xp.md`, `especialista-forms.md`, `especialista-instrumentos.md`, `guardian-consistencia.md`, `ingeniero-sivac.md`, `investigador-bibliografico.md`, `jurado-revisor.md`, `maquetador-docx.md`, `redactor-academico.md`, `verificador-integridad.md`).
  - `.claude/skills/`: 21 directorios de skills (17 especializadas y 4 utilitarias).
  - `.claude/hooks/`: 3 scripts Node.js CommonJS (`pretooluse_blocker.cjs`, `session_start.cjs`, `handoff_reminder.cjs`).
  - `.claude/rules/`: 4 reglas canónicas en Markdown (`01_seguridad.md`, `02_metodologia_dec007.md`, `03_estilo_academico_apa7.md`, `04_protocolo_agentes.md`).
  - `.claude/schemas/`: 3 esquemas JSON Draft 2020-12 (`comision.schema.json`, `handoff.schema.json`, `quality_gates.schema.json`).
  - `.claude/settings.json`: Permisos de carpetas adicionales (`obsidian_vault`, `syncova`) y configuración de hooks para Claude Code.
  - `.claude/settings.local.json`: Claves API protegidas (`FIRECRAWL_API_KEY`, `YDC_API_KEY`).
  - `.claude/workflows/`: Script consolidado `sivac-scripts-especializados.js`.
  - `.claude/commands/`: **No existe** (sin slash commands personalizados en Claude).
- **Directorio `.factory/` en el Proyecto:**
  - **INEXISTENTE**. No existe ninguna carpeta `.factory/` en el árbol de trabajo. Todo el soporte de Droid se apoya en la configuración global de usuario.
- **Capas Funcionales de Datos y Código:**
  - `referencias/`: Insumos inmutables (modelos de tesis UNAJMA, validaciones, `PROYECTO_TESIS.docx`). Protegido por hook.
  - `datos/`: Subcarpetas `raw/`, `processed/`, `plantillas/`, `schemas/` y `_cuarentena_no_empiricos/`.
  - `scripts/`: Subcarpetas `agentes/` (11 scripts deterministas en Python), `compiladores/` (11 constructores capitulares), `utilidades/` (36 utilidades OpenXML/COM), `estadistica/`, `figuras/`.
  - `salidas/`: Documentos compilados (`informe_final_v01.docx`, `.pdf`), instrumentos, figuras, matrices y reportes de jurado.

### 2.2. Nivel de Usuario (`~/.claude/` vs `~/.factory/`)
| Componente | En `~/.claude/` | En `~/.factory/` | Hallazgo y Diagnóstico |
|---|---|---|---|
| **Agentes / Droids** | Carpeta `agents/` vacía | Solo `scrutiny-feature-reviewer.md` y `user-testing-flow-validator.md` | Los agentes de la tesis existen únicamente dentro del proyecto en `.claude/agents/`. Ni Claude Code a nivel global ni Factory Droid los tienen instalados como droids de usuario. |
| **Skills** | 12 skills de tesis instaladas globalmente | 72 skills genéricas/oficiales de Factory Droid | Ninguna de las 21 skills especializadas de la tesis está instalada en `~/.factory/skills/`. Droid no puede descubrirlas globalmente sin importar o referenciar `.claude/skills/`. |
| **Configuración MCP** | Gestionado por extensiones Claude | `~/.factory/mcp.json` con `chrome-devtools`, `zotero`, `firecrawl`, `ydc-server`, `playwright` | Sincronizado recientemente en este reconocimiento. |
| **Hooks** | No configurados globalmente | No configurados globalmente en Droid | Los hooks de seguridad (`pretooluse_blocker.cjs`) solo son interceptados por Claude Code mediante `.claude/settings.json`. |

---

## 3. A2. Ficha Técnica de los 14 Agentes Especializados

### Matriz Sintética de Atributos

| N.° | Nombre del Agente | Squad Funcional | Modelo | Herramientas Asignadas | Skills Declaradas | MCPs Requeridos |
|---|---|---|---|---|---|---|
| 1 | `director-general` | Hub Central | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell, Agent, Skill, Tasks, AskUser | `academic-pipeline`, `matriz-consistencia`, `estructura-tesis-universidad`, `protocolo-obsidian-handoff` | Zotero, Firecrawl, YDC |
| 2 | `investigador-bibliografico` | Squad A | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `zotero-busqueda-academica`, `deep-research`, `apa7-es-tesis`, `redaccion-academica-verificable`, `citacion-exacta-pdf`, `ingreso-fuentes-bibliograficas`, `figuras-de-fuentes-pdf`, `protocolo-obsidian-handoff` | Zotero, YDC, Firecrawl |
| 3 | `verificador-integridad` | Squad A | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `zotero-busqueda-academica`, `academic-paper`, `deep-research`, `apa7-es-tesis`, `redaccion-academica-verificable`, `citacion-exacta-pdf`, `protocolo-obsidian-handoff` | Zotero, Crossref |
| 4 | `guardian-consistencia` | Squad B | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `matriz-consistencia`, `estructura-tesis-universidad`, `apa7-es-tesis`, `protocolo-obsidian-handoff` | Filesystem |
| 5 | `especialista-instrumentos` | Squad B | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `formato-instrumentos-validacion`, `validacion-psicometrica`, `matriz-consistencia`, `protocolo-obsidian-handoff` | Filesystem |
| 6 | `especialista-forms` | Squad B | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `formato-instrumentos-validacion`, `validacion-psicometrica`, `protocolo-obsidian-handoff` | Filesystem |
| 7 | `ingeniero-sivac` | Squad C | sonnet | **Read, Grep, Glob** (Solo lectura) | `context7`, `extraccion-figuras-pdf-docx`, `protocolo-obsidian-handoff` | Context7, Local Repo |
| 8 | `documentador-xp` | Squad C | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `context7`, `extraccion-figuras-pdf-docx`, `redaccion-academica-verificable`, `estructura-tesis-universidad`, `protocolo-obsidian-handoff` | Context7 |
| 9 | `analista-estadistico` | Squad D | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `analisis-estadistico-avanzado`, `validacion-psicometrica`, `xlsx`, `dataviz`, `protocolo-obsidian-handoff` | Python/R Kernel |
| 10 | `analista-documental` | Squad E | sonnet | Read, Grep, Glob, Bash, PowerShell | `docx`, `pdf`, `xlsx`, `estructura-tesis-universidad`, `extraccion-figuras-pdf-docx`, `protocolo-obsidian-handoff` | Filesystem |
| 11 | `redactor-academico` | Squad E | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `redaccion-academica-verificable`, `academic-paper`, `apa7-es-tesis`, `estructura-tesis-universidad`, `matriz-consistencia`, `citacion-exacta-pdf`, `protocolo-obsidian-handoff` | Zotero |
| 12 | `maquetador-docx` | Squad E | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `docx`, `pdf`, `tablas-quirurgicas-docx-apa7`, `referencias-nativas-docx-apa7`, `estructura-tesis-universidad`, `extraccion-figuras-pdf-docx`, `figuras-de-fuentes-pdf`, `protocolo-obsidian-handoff` | Word COM, Python |
| 13 | `curador-cerebro` | Squad F | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `protocolo-obsidian-handoff` | Obsidian Vault |
| 14 | `jurado-revisor` | Squad F | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `academic-paper-reviewer`, `matriz-consistencia`, `estructura-tesis-universidad`, `formato-instrumentos-validacion`, `protocolo-obsidian-handoff` | Filesystem |

### Análisis Crítico por Agente
1. **Sobreasignación de privilegios:** Agentes como `guardian-consistencia`, `especialista-instrumentos` o `jurado-revisor` tienen acceso a `Bash` y `PowerShell` a pesar de que su función es analítica y documental en Markdown. Solo requieren herramientas de archivo (`Read`, `Write`, `Edit`, `Grep`, `Glob`).
2. **Pseudo-skills que son MCPs:** Tanto `ingeniero-sivac` como `documentador-xp` tienen listado `context7` dentro de `skills: [...]`, cuando en realidad `context7` es un servidor MCP, no una skill con carpeta `SKILL.md`.
3. **Discrepancia en modelos:** `AGENTS.md` prescribe modelo `opus` para toda la granja, pero el frontmatter de los 13 subagentes fija `model: sonnet` y `director-general` fija `model: opus`.
4. **Disciplina de handoff:** Todos los agentes declaran `protocolo-obsidian-handoff`, lo que garantiza que al concluir una tarea depositen su reporte en `08_SISTEMA_Y_AGENTES/handoffs/`.

---

## 4. A3. Radiografía del Orquestador GOD (`director-general`)

- **Patrón de Descomposición:** Opera bajo el esquema formal de comisión (`.claude/schemas/comision.schema.json`): define tarea, fase, squad, subagente, entradas, salida esperada, restricciones y criterio de éxito.
- **Enrutamiento:** Distribuye de forma radial hacia los Squads A–F. Ningún subagente puede comisionar a otro subagente.
- **Control de Estado:** Lee y actualiza `C:\MisInvestigaciones\obsidian_vault\00_SISTEMA\ESTADO_TESIS.md`. Este archivo es la **única fuente de verdad** del avance capitular y metodológico.
- **Supervisión de Quality Gates:** Aplica compuertas de calidad (QG-0 a QG-9). No permite avanzar a una fase sin la aprobación de la compuerta previa y la autorización del tesista humano.
- **Riesgos y Vicios Detectados:**
  - *Tentación de Ejecución Monolítica:* El Director General posee todas las herramientas (`Write`, `Edit`, `PowerShell`). En ocasiones pasadas ha modificado scripts Python y compilado documentos directamente en lugar de delegar en `maquetador-docx` o `redactor-academico`.
  - *Inflación de Contexto:* En sesiones largas, el contexto acumulado de múltiples lecturas de código de compilación desgasta la memoria de la ventana activa. La delegación en subagentes (`Task` o `Agent`) es indispensable para mantener limpia la sesión principal.

---

## 5. A4. Flujo Real Actual de Trabajo

### Secuencia Operativa de Punta a Punta
1. **Tesista Humano:** Emite directiva o requerimiento en la sesión principal (ej. "Revisar coherencia del Capítulo IV").
2. **Director General (Agente GOD):**
   - Consulta `ESTADO_TESIS.md` y `REGLAS.md`.
   - Formula el contrato de comisión formal (`comision.schema.json`).
   - Delega la tarea al subagente especialista mediante `Agent` (en Claude Code) o ejecuta el script especializado asociado en `scripts/agentes/`.
3. **Subagente Especialista:**
   - Lee insumos en `referencias/`, `salidas/` o notas de Obsidian.
   - Aplica sus skills asignadas y herramientas MCP.
   - Genera entregable o reporte de auditoría.
   - Redacta el handoff en `08_SISTEMA_Y_AGENTES/handoffs/AAAA-MM-DD_<agente>_<tarea>.md` y actualiza su bitácora en `08_SISTEMA_Y_AGENTES/bitacoras/<agente>.md`.
4. **Director General:**
   - Recibe el handoff y evalúa la compuerta de calidad.
   - Si requiere cambios editoriales, comisiona a `maquetador-docx` para recompilar `informe_final_v01.docx`.
   - Comisiona a `verificador-integridad` o `jurado-revisor` para auditoría cruzada.
   - Actualiza `ESTADO_TESIS.md` a través de `curador-cerebro`.
   - Solicita aprobación formal al Tesista Humano.

*(Ver diagrama formal en `docs/analisis/flujo_actual.mmd`).*

---

## 6. A5. El Cerebro de Obsidian (`C:\MisInvestigaciones\obsidian_vault`)

### 6.1. Estructura de Carpetas Canónicas
- `00_SISTEMA/`: Gobernanza viva (`ESTADO_TESIS.md`, `DECISIONES.md`, `REGLAS.md`, `GLOSARIO.md`, `INVENTARIO_SKILLS.md`).
- `01_MOCS/`: Mapas de Contenido de la tesis.
- `02_PROYECTOS/`: Hitos y sprints de investigación.
- `03_CONCEPTOS_ATOMICOS/`: Notas atómicas Zettelkasten sobre conceptos clave (TAM, XP, ISO 25010, etc.).
- `04_LITERATURA_Y_FUENTES/`: Catálogo maestro Zotero (`CATALOGO_MAESTRO_FUENTES_ZOTERO_SIVAC.md`), 26 PDFs indexados físicamente y notas bibliográficas con `@citekey`.
- `05_MODELOS_Y_REFERENCIAS/`: Desglose estructural de tesis modelo UNAJMA (Jhon 2026, Fany 2024) y paquete Cóndor Tinoco.
- `06_METODOLOGIA_E_INSTRUMENTOS/`: Especificación técnica de fichas de observación, guías de cotejo y cuestionario TAM.
- `07_ESTADISTICA_Y_DATOS/`: Protocolos inferenciales, diseño muestral y baremos.
- `08_SISTEMA_Y_AGENTES/`:
  - `bitacoras/`: 10 archivos de bitácora individual por agente.
  - `handoffs/`: 42 notas de relevo fechadas y tipificadas.
  - `revisiones/`: Dictámenes de jurado y auditorías.
- `09_CANVAS_Y_DIAGRAMAS/`: Diagramas visuales en Canvas de Obsidian.
- `99_INBOX/`: Bandeja de entrada para procesar.

### 6.2. Evaluación de Disciplina y Enlaces
- **Frontmatter YAML:** Ampliamente adoptado en `00_SISTEMA` y `08_SISTEMA_Y_AGENTES` con campos `tipo`, `fase`, `agente`, `fecha`, `tags`.
- **Wikilinks:** Uso intensivo de `[[Nombre_Nota]]` para navegación interna y MOCs.
- **Acceso:** Ambos entornos (Claude Code y Factory Droid) acceden al vault directamente mediante el sistema de archivos local (`fs` / herramientas de lectura y edición de archivos), sin depender de plugins de red ni servidores HTTP locales de Obsidian.

---

## 7. A6. Flujo y Pipeline DOCX

### 7.1. Arquitectura de Ensamblaje Editorial
A diferencia de flujos tradicionales que convierten de Markdown a DOCX mediante Pandoc (lo que destruye estilos institucionales y corrompe ecuaciones complejas), SIVAC-THESIS-LAB utiliza un motor programático OpenXML nativo:
- **Ensamblador Maestro:** `scripts/compiladores/compilar_informe_final_docx.py`.
- **Constructores Capitulares:** `secciones_preliminares.py` y `capitulo1_builder.py` a `capitulo6_builder.py`.
- **Motor Quirúrgico:** `scripts/utilidades/docx_quirurgico.py` y `docx_utilidades.py`.
  - Manipulación directa del árbol XML (`word/document.xml`).
  - Inserción de ecuaciones OMML nativas `<m:oMath>` a partir de MathML estándar.
  - Generación de tablas APA 7 con tres bordes horizontales (borde superior, encabezado inferior y borde final) sin cuadrícula vertical, con ancho estricto de `8788 dxa`.
  - Inserción de imágenes con relación de aspecto preservada y resolución nativa a 300 DPI.
  - Creación de secciones desvinculadas: Sección 1 (preliminares en números romanos) y Sección 2 (cuerpo principal en arábigos desde 1).

### 7.2. Automatización COM de Word
Para la actualización de los campos nativos de Word (Tabla de Contenido `TOC`, Índice de Tablas, Índice de Figuras y numeración de páginas), se utiliza Microsoft Word vía COM (`win32com.client`):
- `test_word_com_clean.py` / `kill_hung_word.py`.
- Actualiza campos y exporta a PDF idéntico al renderizado final de impresión.

---

## 8. Conclusiones y Estado de Preparación para Fase B

El sistema posee un nivel de detalle metodológico e ingenieril excepcional. Su principal debilidad no radica en la lógica científica ni en la calidad del documento generado, sino en la **falta de una capa de compatibilidad formal que permita a Factory Droid orquestar y comisionar a estos mismos agentes de manera nativa sin salirse de la constitución de `.claude/`**.

Se concluye la **Fase A (Reconocimiento)**. El sistema se encuentra listo para iniciar la **Fase B (Verificación de Compatibilidad `.claude/` ↔ Droid en Máquina)**.
