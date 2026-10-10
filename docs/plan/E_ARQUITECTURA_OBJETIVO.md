# PLAN DE ARQUITECTURA OBJETIVO (FASE E1–E8)
## Sistema Multiagente Autónomo SIVAC-THESIS-LAB v3.0
> **Proyecto:** SIVAC-THESIS-LAB — Granja de Agentes de Investigación Científica  
> **Universidad:** Universidad Nacional José María Arguedas (UNAJMA) — EPIS  
> **Tesista / Autor:** Bach. José Luis Quispe León | **Asesora:** Dra. Norma Lorena Catacora Flores  
> **Fecha:** 2026-10-09  
> **Principio Rector:** `.claude/` es la ÚNICA fuente de verdad canónica. `.factory/` es una capa generada automáticamente y 100% reproducible.

---

## 1. E1. Estructura Objetivo del Repositorio

```text
sivac/ (Espacio de Trabajo Principal)
├── CLAUDE.md                            # 🏛️ CANÓNICO: Constitución operativa concisa (reglas globales + mapa)
├── AGENTS.md                            # 🤖 PUENTE: Enlace estructurado hacia CLAUDE.md y mapa de squads
├── .mcp.json                            # 🔌 CANÓNICO: Configuración de servidores MCP compartidos
├── requirements.txt                     # 📦 Dependencias científicas y OpenXML
├── .gitignore                           # 🛡️ Exclusiones de seguridad
│
├── .claude/                             # 🧠 FUENTE DE VERDAD ABSOLUTA (SE EDITA EXCLUSIVAMENTE AQUÍ)
│   ├── agents/                          # 14 agentes canónicos con frontmatter estandarizado
│   ├── skills/                          # 21 skills especializadas con SKILL.md y referencias
│   ├── hooks/                           # Scripts Node.js / Python reutilizables por ambas CLIs
│   ├── rules/                           # 4 reglas modulares (Seguridad, Metodología, APA 7, Protocolo)
│   ├── schemas/                         # Esquemas JSON de comisión, handoff y quality gates
│   ├── settings.json                    # Permisos y hooks de Claude Code
│   └── settings.local.json              # Claves API y secretos protegidos (ignorado en git)
│
├── .factory/                            # ⚙️ CAPA GENERADA / REPRODUCIBLE (NO EDITAR DIRECTAMENTE)
│   ├── droids/                          # <!-- GENERADO desde .claude/agents/ --> (14 droids DroidValidator-ready)
│   ├── skills/                          # <!-- ENLAZADO vía Junction o sincronizado desde .claude/skills/ -->
│   ├── hooks.json                       # <!-- GENERADO desde .claude/settings.json y .claude/hooks/ -->
│   └── mcp.json                         # <!-- GENERADO desde .mcp.json y settings.local.json -->
│
├── scripts/                             # ⚙️ HERRAMIENTAS Y AUTOMATIZACIÓN
│   ├── sync_factory.py                  # 🔄 Generador determinista de compatibilidad .claude/ -> .factory/
│   ├── validar_docx.py                  # 📋 Validador quirúrgico de estilos, tablas y ecuaciones OpenXML
│   ├── validar_frontmatter.py           # 🔍 Auditor de integridad de metadatos YAML
│   ├── agentes/                         # Scripts deterministas ejecutados por los agentes
│   ├── compiladores/                    # Ensamblador maestro y constructores capitulares
│   └── utilidades/                      # docx_quirurgico.py y utilidades COM/OpenXML
│
├── referencias/                         # 📚 INSUMOS INMUTABLES (SOLO LECTURA)
│   ├── modelos_tesis/                   # Tesis modelo UNAJMA (Jhon 2026, Fany 2024)
│   ├── modelos_validacion/              # Formatos oficiales Dr. Cóndor Tinoco
│   └── proyecto_base/                   # Proyecto original respaldado
│
├── datos/                               # 📊 PIPELINE DE DATOS Y MEDICIÓN (Muestra censal n=14)
│   ├── raw/                             # Datos brutos de campo (inmutables una vez ingresados)
│   ├── processed/                       # Tabulaciones listas para contrastes
│   └── plantillas/                      # Matrices vacías para recolección en campo
│
├── salidas/                             # 🎯 ENTREGABLES GENERADOS
│   ├── documentos/                      # informe_final_vNN.docx y .pdf oficiales
│   ├── instrumentos/                    # Expedientes de validación y fichas
│   └── reportes_jurado/                 # Dictámenes colegiados UNAJMA
│
├── docs/                                # 📖 DOCUMENTACIÓN DEL SISTEMA MULTIAGENTE
│   ├── analisis/                        # Informes de Reconocimiento, Compatibilidad y Diagnóstico
│   ├── plan/                            # Plan de Arquitectura y Migración
│   ├── EQUIVALENCIAS_PLATAFORMA.md      # Manual de traducción Claude Code <-> Factory Droid
│   └── CHANGELOG.md                     # Registro histórico de versiones
│
└── _archive/                            # 📦 HISTÓRICO Y ARTEFACTOS OBSOLETOS
```

---

## 2. E2. Equipo de Agentes Objetivo (Especialización y Mínimo Privilegio)

Se conservan y perfeccionan los **14 agentes especializados** organizados en la topología Hub-and-Spoke. Se erradica la sobreasignación de herramientas de shell (`Execute`), limitándolas estrictamente a los roles que compilan código o calculan estadísticas.

| Squad | Agente | Responsabilidad Única | Lo que NUNCA hace | Herramientas (Principio de Mínimo Privilegio) | MCPs |
|---|---|---|---|---|---|
| **Hub Central** | **`director-general`** (GOD) | Planifica por fases, comisiona formalmente, evalúa compuertas, mantiene `ESTADO_TESIS.md` y consulta al tesista | **Nunca redacta contenido capitular** ni compila documentos en solitario | `Read`, `Create`, `Edit`, `Grep`, `Glob`, `Execute`, `Task`, `Skill`, `TodoWrite`, `AskUser` | `zotero`, `ydc-server`, `firecrawl` |
| **Squad A** | **`investigador-bibliografico`** | Búsqueda sistemática, selección, lectura de papers y fichaje en Obsidian | **Nunca redacta capítulos de la tesis** | `Read`, `Create`, `Edit`, `Grep`, `Glob` | `zotero`, `ydc-server`, `firecrawl` |
| **Squad A** | **`verificador-integridad`** | Auditoría biunívoca 1:1 (cuerpo vs referencias), verificación de DOIs y anti-alucinaciones | **Nunca redacta contenido nuevo** ni valida su propio trabajo | `Read`, `Create`, `Edit`, `Grep`, `Glob`, `Execute` (scripts python locales) | `zotero` |
| **Squad B** | **`guardian-consistencia`** | Custodio de la matriz de consistencia, operacionalización y las 3 dimensiones DEC-007 | **Nunca modifica código de software** ni realiza búsquedas bibliográficas | `Read`, `Create`, `Edit`, `Grep`, `Glob` | Filesystem |
| **Squad B** | **`especialista-instrumentos`** | Diseño psicométrico de fichas de tiempos, guías de cotejo y cuestionario TAM; cálculo de V de Aiken e IVC | **Nunca redacta capítulos teóricos** | `Read`, `Create`, `Edit`, `Grep`, `Glob` | Filesystem |
| **Squad B** | **`especialista-forms`** | Digitalización de instrumentos en Google Forms / Apps Script y validación de recolección | **Nunca modifica la operacionalización de variables** | `Read`, `Create`, `Edit`, `Grep`, `Glob` | `playwright` |
| **Squad C** | **`ingeniero-sivac`** | Auditoría técnica de código de `syncova` (Prisma, PostgreSQL, Express, React) en **MODO ESTRICTO DE SOLO LECTURA** | **NUNCA ESCRIBE NI MODIFICA** código ni archivos | `Read`, `Grep`, `Glob` (Estricto Solo Lectura) | `context7` |
| **Squad C** | **`documentador-xp`** | Redacción técnica de la sección 3.3 (Metodología XP, 76 historias de usuario, diagramas UML, iteraciones 1 a 4) | **Nunca inventa funcionalidades** no presentes en el código real | `Read`, `Create`, `Edit`, `Grep`, `Glob` | `context7`, `playwright` |
| **Squad D** | **`analista-estadistico`** | Procesamiento bioestadístico reproducible (Shapiro-Wilk, Wilcoxon, t de Student, Cohen) en Python/R | **Nunca inventa ni simula datos** sin respaldo en `datos/raw/` | `Read`, `Create`, `Edit`, `Grep`, `Glob`, `Execute` | Python/R Kernel |
| **Squad E** | **`analista-documental`** | Inspección profunda OpenXML/PDF de modelos UNAJMA (Jhon 2026, Fany 2024) y control de márgenes/estilos | **Nunca redacta prosa científica** | `Read`, `Create`, `Edit`, `Grep`, `Glob`, `Execute` | Filesystem |
| **Squad E** | **`redactor-academico`** | Redacción de la prosa científica en español formal impersonal bajo estándar APA 7 desde notas de Obsidian | **Nunca inventa citas** ni altera el diseño metodológico | `Read`, `Create`, `Edit`, `Grep`, `Glob` | `zotero` |
| **Squad E** | **`maquetador-docx`** | **Único agente autorizado** para compilar el documento maestro DOCX mediante `docx_quirurgico.py` y Word COM | **Nunca altera el sentido o contenido** de los textos aprobados | `Read`, `Create`, `Edit`, `Grep`, `Glob`, `Execute` | Word COM, Python |
| **Squad F** | **`curador-cerebro`** | Custodio del vault de Obsidian: taxonomía, frontmatter, enlaces `[[wikilinks]]`, estado y bitácoras | **Nunca redacta contenido académico** | `Read`, `Create`, `Edit`, `Grep`, `Glob` | Obsidian Vault |
| **Squad F** | **`jurado-revisor`** | Tribunal simulado UNAJMA (5 jueces + Abogado del Diablo); evaluación ciega con rúbrica vigesimal de 20 puntos | **Nunca aprueba capítulos** con inconsistencias metodológicas | `Read`, `Create`, `Edit`, `Grep`, `Glob` | Filesystem |

---

## 3. E3. Protocolo de Comunicación y Gobernanza Multi-CLI

### 3.1. Contrato de Comisión Formal
El Director General emite una comisión formal estructurada en el prompt:
```text
TAREA: <Acción concreta, específica y acotada>
FASE: <F0 a F9 según ESTADO_TESIS.md>
SQUAD: <Squad A / B / C / D / E / F>
SUBAGENTE: <nombre-agente>
ENTRADAS: <Rutas exactas de archivos base o notas de Obsidian>
SALIDA ESPERADA: <Ruta y formato exacto del entregable>
RESTRICCIONES: <Reglas innegociables aplicables (ej. DEC-007, Regla 01)>
CRITERIO DE ÉXITO: <Métrica o condición objetiva de terminación>
```

### 3.2. Contrato de Handoff Estandarizado (en Obsidian)
Todo subagente deposita obligatoriamente su informe de relevo en:  
`C:\MisInvestigaciones\obsidian_vault\08_SISTEMA_Y_AGENTES\handoffs\AAAA-MM-DD_<agente>_<tarea>.md`
Con frontmatter estandarizado:
```yaml
---
tipo: handoff
tarea_id: <identificador-unico>
fase: <F0-F9>
agente: <nombre-agente>
fecha: AAAA-MM-DD
estado: completado | parcial | bloqueado
entradas: [<rutas>]
salidas: [<rutas>]
revisor_asignado: <agente-validador>
---
```

### 3.3. Validación Cruzada Obligatoria
Ningún entregable pasa de fase sin ser revisado por un agente independiente:
- Lo redactado por `redactor-academico` $\longrightarrow$ auditado por `verificador-integridad` (citas 1:1) y `guardian-consistencia` (isomorfismo).
- Lo documentado por `documentador-xp` $\longrightarrow$ auditado por `ingeniero-sivac` (fidelidad al código de `syncova`).
- Lo compilado por `maquetador-docx` $\longrightarrow$ auditado por `analista-documental` (geometría OpenXML) y evaluado por `jurado-revisor` (rúbrica 20 pts).

### 3.4. Regla de Escalado
Si un entregable recibe **2 rechazos consecutivos** en la validación cruzada:
1. El Director General detiene el ciclo automático.
2. Genera un informe de discrepancia en Obsidian.
3. Escala la decisión al **Tesista Humano** en la sesión principal mediante `AskUser`.

---

## 4. E4. Skills Especializadas (Catálogo Canónico en `.claude/skills/`)

Las 21 skills se agrupan en dominios funcionales claros y se enlazan directamente a `.factory/skills/`:

1. **Metodología y Consistencia:** `matriz-consistencia`, `estructura-tesis-universidad`, `validacion-psicometrica`, `formato-instrumentos-validacion`.
2. **Literatura e Integridad Académica:** `zotero-busqueda-academica`, `deep-research`, `citacion-exacta-pdf`, `ingreso-fuentes-bibliograficas`, `apa7-es-tesis`.
3. **Redacción Científica y Revisión:** `redaccion-academica-verificable`, `academic-paper`, `academic-paper-reviewer`.
4. **Ingeniería OpenXML y Editorial:** `tablas-quirurgicas-docx-apa7`, `referencias-nativas-docx-apa7`, `extraccion-figuras-pdf-docx`, `figuras-de-fuentes-pdf`.
5. **Estadística y Visualización:** `analisis-estadistico-avanzado`, `dataviz`.
6. **Gobernanza y Memoria:** `academic-pipeline`, `protocolo-obsidian-handoff`.

---

## 5. E5. El Cerebro de Obsidian como Memoria Persistente

Estructura canónica unificada bajo estándares Zettelkasten y PARA:
```text
C:\MisInvestigaciones\obsidian_vault/
├── 00_SISTEMA/           # Estado vivo, decisiones (ADR), glosario y verificación
├── 01_MOCS/              # Mapas de Contenido de la tesis
├── 02_PROYECTOS/         # Fases operativas y sprints
├── 03_CONCEPTOS_ATOMICOS/# Notas atómicas (TAM, XP, ISO 25010, Kardex, Vacunas)
├── 04_LITERATURA_Y_FUENTES/# Catálogo maestro Zotero y fichas de lectura con @citekey
├── 05_MODELOS_Y_REFERENCIAS/# Modelos oficiales UNAJMA desglosados
├── 06_METODOLOGIA_E_INSTRUMENTOS/# Especificación técnica de instrumentos
├── 07_ESTADISTICA_Y_DATOS/# Protocolos bioestadísticos
├── 08_SISTEMA_Y_AGENTES/ # Bitácoras individuales, handoffs y revisiones de jurado
├── 09_CANVAS_Y_DIAGRAMAS/# Diagramas visuales en Canvas
├── 99_INBOX/             # Bandeja de entrada de insumos no procesados
└── _adjuntos/            # Gráficos y capturas vinculadas
```

---

## 6. E6. Pipeline Editorial DOCX Nativo y Cirugía OpenXML

1. **Insumo Canónico:** Notas estructuradas y validadas en Obsidian.
2. **Transformación:** Constructores capitulares dedicados (`scripts/compiladores/capituloX_builder.py`).
3. **Inyección OpenXML Nativa (`docx_quirurgico.py`):**
   - Ecuaciones matemáticas en MathML transformadas a `<m:oMath>` centrado.
   - Tablas nativas APA 7 de tres líneas con ancho fijo de `8788 dxa` y sin fórmulas en celdas.
   - Secciones desvinculadas: Sección 1 (romanos `i, ii, iii...`) y Sección 2 (arábigos `1, 2, 3...`).
4. **Compilación y Actualización COM:**
   - Word COM (`win32com.client`) actualiza la Tabla de Contenido (TOC), Índice de Tablas, Índice de Figuras y exporta a `informe_final_vNN.pdf`.
   - Control de procesos con timeout y limpieza vía `kill_hung_word.py`.
5. **Auditoría Post-Generación:** `scripts/utilidades/auditor_docx_apa7.py` verifica 0 errores antes de dar por buena la compilación.

---

## 7. E7. Sistema Unificado de Hooks de Seguridad y Gobernanza

Los scripts en `.claude/hooks/` operan como controladores universales llamados por ambas plataformas:

1. **`pretooluse_blocker.cjs` (PreToolUse):**
   - Intercepta `Create`, `Edit`, `Write` y comandos de shell.
   - Bloquea cualquier modificación a `C:\Proyectos\syncova` (solo lectura) y `referencias/` (inmutables).
   - Retorna código de salida `2` en Droid para forzar el bloqueo con mensaje explicativo a la CLI.
2. **`session_start.cjs` (SessionStart):**
   - Despliega el resumen de `ESTADO_TESIS.md` al inicializar la sesión para que el orquestador conozca la fase activa.
3. **`handoff_reminder.cjs` (SubagentStop / Stop):**
   - Verifica que el subagente haya registrado su nota de relevo en `08_SISTEMA_Y_AGENTES/handoffs/` antes de concluir su ciclo.

---

## 8. E8. Fases de la Tesis y Quality Gates Institucionales

| Fase | Denominación | Agentes Clave | Entregables Requeridos | Validador Cruzado | Quality Gate |
|---|---|---|---|---|---|
| **F0** | Ecosistema y Granja | `director-general`, `curador-cerebro` | Sincronización `.factory/`, scripts y repositorios | `analista-documental` | **QG-0 (Ecosistema Verificado)** |
| **F1** | Diagnóstico y Brechas | `analista-documental`, `director-general` | `desglose_proyecto_base.json` | `guardian-consistencia` | **QG-1 (Diagnóstico Aprobado)** |
| **F2** | Metodología y Matrices | `guardian-consistencia`, `especialista-instrumentos` | Matriz de consistencia v3.0, 3 dimensiones DEC-007 | `jurado-revisor` | **QG-2 (Isomorfismo Metodológico)** |
| **F3** | Marco Teórico y Citas | `investigador-bibliografico`, `redactor-academico` | Capítulos I y II compilados, 27+ citas Zotero | `verificador-integridad` | **QG-3 (Citas 1:1 Verificadas)** |
| **F4** | Ingeniería XP (Sec. 3.3) | `ingeniero-sivac`, `documentador-xp` | Sección 3.3 con 76 historias de usuario y diagramas | `ingeniero-sivac` | **QG-4 (Trazabilidad 1:1 syncova)** |
| **F5** | Instrumentos de Medición | `especialista-instrumentos`, `especialista-forms` | Expediente para expertos, V de Aiken e IVC > 0.80 | `jurado-revisor` | **QG-5 (Blindaje Psicométrico)** |
| **F6** | Trabajo de Campo | `especialista-forms`, `analista-estadistico` | Datos reales pretest/postest en `datos/raw/` | `guardian-consistencia` | **QG-6 (Calidad de Datos n=14)** |
| **F7** | Resultados (Capítulo V) | `analista-estadistico`, `redactor-academico` | Tablas descriptivas e inferenciales en Word | `guardian-consistencia` | **QG-7 (Normalidad e Inferencia)** |
| **F8** | Discusión y Conclusiones | `redactor-academico`, `investigador-bibliografico` | Capítulo VI, Conclusiones 1:1 con objetivos | `jurado-revisor` | **QG-8 (Coherencia Explicativa)** |
| **F9** | Ensamblaje y Sustentación | `maquetador-docx`, `director-general` | `informe_final_definitivo.docx` y `.pdf`, slides | `jurado-revisor` + Tesista | **QG-9 (Aprobación UNAJMA)** |
