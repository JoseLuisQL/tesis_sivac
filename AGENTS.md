# MATRIZ MAESTRA DE LA GRANJA DE AGENTES — SIVAC-THESIS-LAB
> **Ecosistema Multi-Agente de Investigación Científica para el Informe Final de Tesis**  
> **Escuela Profesional de Ingeniería de Sistemas — Universidad Nacional José María Arguedas (UNAJMA)**  
> **Topología:** Hub-and-Spoke (Estrella Jerárquica Radial) | **Orquestador:** Agente GOD (`director-general`)  
> **Constitución Operativa:** Consultar [[CLAUDE.md]] | **Reglas Canónicas:** Consultar `.claude/rules/*.md`

---

## 1. Topología del Sistema y Principio de Mando

```
                               ┌────────────────────────────────────────────────────────┐
                               │               TESISTA HUMANO (Investigador)            │
                               │        [Última Autoridad - Aprobaciones de Fase]       │
                               └───────────────────────────▲────────────────────────────┘
                                                           │ Aprobación / Feedback
                               ┌───────────────────────────▼────────────────────────────┐
                               │       AGENTE GOD / DIRECTOR DE TESIS SENIOR            │
                               │               (Sesión Principal / Lead)                │
                               │   - Orquestador Maestro de la Constitución (CLAUDE.md) │
                               │   - Refinamiento Cognitivo de Prompts Débiles          │
                               │   - Memoria Viva y Persistente en Obsidian             │
                               │   - Rescate de Pendientes y Sugerencias Proactivas     │
                               │   - Comisionador Formal Radial a 13 Subagentes (A-F)   │
                               │   - Supervisor de Quality Gates y Cirugía OpenXML      │
                               └───────────────────────────┬────────────────────────────┘
                                                           │ Comisiones / Handoffs
         ┌───────────────────┬─────────────────────────────┼─────────────────────────────┬───────────────────┐
         │                   │                             │                             │                   │
┌────────▼─────────┐┌────────▼─────────┐         ┌─────────▼──────────┐        ┌─────────▼─────────┐┌────────▼─────────┐
│     SQUAD A      ││     SQUAD B      │         │      SQUAD C       │        │      SQUAD D      ││     SQUAD E      │
│   Evidencia y    ││   Metodología    │         │   Ingeniería de    │        │  Bioestadística   ││   Redacción y    │
│  Bibliometría    ││  y Psicometría   │         │  Software SIVAC    │        │  e Inferencia     ││  Maquetación     │
├──────────────────┤├──────────────────┤         ├────────────────────┤        ├───────────────────┤├──────────────────┤
│• investigador-   ││• guardian-       │         │• ingeniero-sivac   │        │• analista-        ││• analista-       │
│  bibliografico   ││  consistencia    │         │  (Solo Lectura)    │        │  estadistico      ││  documental      │
│• verificador-    ││• especialista-   │         │• documentador-xp   │        │                   ││• redactor-       │
│  integridad      ││  instrumentos    │         │                    │        │                   ││  academico       │
│                  ││• especialista-   │         │                    │        │                   ││• maquetador-     │
│                  ││  forms           │         │                    │        │                   ││  docx            │
└──────────────────┘└──────────────────┘         └────────────────────┘        └───────────────────┘└──────────────────┘
                                                           │
                                                 ┌─────────▼──────────┐
                                                 │      SQUAD F       │
                                                 │ Gobernanza, Memoria│
                                                 │ y Evaluación       │
                                                 ├────────────────────┤
                                                 │• curador-cerebro   │
                                                 │• jurado-revisor    │
                                                 │  (Simulador UNAJMA)│
                                                 └────────────────────┘
```

**Regla de Ejecución:** En Claude Code los subagentes no pueden delegar en otros subagentes. Todo flujo de trabajo es estrictamente radial entre el **Director General** (sesión principal) y cada **Subagente Especialista** (`.claude/agents/*.md`).

---

## 2. Catálogo Oficial de Squads y Agentes

| Squad | Agente | Rol Operativo | Modelo | Herramientas Principales | Skills Asignadas |
|---|---|---|---|---|---|
| **Hub Central** | `director-general` | Director de Tesis Senior / Agente GOD (Refinamiento cognitivo de prompts débiles, articulación de memoria viva y persistente en Obsidian, rescate de pendientes metodológicos, orquestador maestro y comisionador formal radial a los 13 subagentes de los Squads A-F) | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell, Agent, Skill, Tasks | `academic-pipeline`, `protocolo-obsidian-handoff`, `matriz-consistencia`, `estructura-tesis-universidad` |
| **Squad A** | `investigador-bibliografico` | Búsqueda y síntesis sistemática | sonnet | Read, Write, Edit, Grep, Glob | `deep-research`, `zotero-busqueda-academica`, `apa7-es-tesis` |
| **Squad A** | `verificador-integridad` | Auditoría 1:1 y anti-alucinaciones | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `academic-paper` (citation-check), `deep-research` (fact-check) |
| **Squad B** | `guardian-consistencia` | Custodio isomórfico (3 dims DEC-007) | sonnet | Read, Write, Edit, Grep, Glob | `matriz-consistencia`, `estructura-tesis-universidad` |
| **Squad B** | `especialista-instrumentos` | Diseño psicométrico y juicio expertos | sonnet | Read, Write, Edit, Grep, Glob | `formato-instrumentos-validacion`, `validacion-psicometrica` |
| **Squad B** | `especialista-forms` | Formularios digitales y Apps Script | sonnet | Read, Write, Edit, Grep, Glob | `formato-instrumentos-validacion`, `validacion-psicometrica` |
| **Squad C** | `ingeniero-sivac` | Auditor de software (SOLO LECTURA) | sonnet | **Solo Lectura:** Read, Grep, Glob | `extraccion-figuras-pdf-docx`, `protocolo-obsidian-handoff` (MCP: `context7`) |
| **Squad C** | `documentador-xp` | Redactor de sección 3.3 (XP, UML) | sonnet | Read, Write, Edit, Grep, Glob | `redaccion-academica-verificable`, `extraccion-figuras-pdf-docx` (MCP: `context7`) |
| **Squad D** | `analista-estadistico` | Bioestadístico y contrastes ($n=14$) | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `analisis-estadistico-avanzado`, `dataviz`, `xlsx` |
| **Squad E** | `analista-documental` | Desglose estructural de modelos UNAJMA | sonnet | Read, Grep, Glob, Bash, PowerShell | `docx`, `pdf`, `xlsx`, `estructura-tesis-universidad` |
| **Squad E** | `redactor-academico` | Redactor en prosa científica APA 7 | sonnet | Read, Write, Edit, Grep, Glob | `academic-paper`, `apa7-es-tesis`, `redaccion-academica-verificable` |
| **Squad E** | `maquetador-docx` | Compilador OpenXML desvinculado | sonnet | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `tablas-quirurgicas-docx-apa7`, `referencias-nativas-docx-apa7`, `docx` |
| **Squad F** | `curador-cerebro` | Custodio de Obsidian (No destrucción) | sonnet | Read, Write, Edit, Grep, Glob | `protocolo-obsidian-handoff` |
| **Squad F** | `jurado-revisor` | Tribunal simulado UNAJMA (20 pts) | sonnet | Read, Write, Edit, Grep, Glob | `academic-paper-reviewer`, `matriz-consistencia` |

---

## 3. Protocolos de Comisión y Handoff

### 3.0. Loop de Refinamiento Cognitivo de Prompts Débiles y Memoria Viva Previa
Antes de emitir cualquier contrato de comisión, el Director General activa obligatoriamente el **Loop de Refinamiento Cognitivo**:
1. **Diagnóstico de la Intención Profunda:** Decodifica el requerimiento científico o técnico subyacente ante solicitudes breves, coloquiales o ambiguas del tesista (ej. *"revisa esto"*, *"avanza el cap 5"*, *"arregla la tabla"*).
2. **Cruce con la Memoria Viva de Obsidian:** Consulta obligatoria de `00_SISTEMA/ESTADO_TESIS.md`, `00_SISTEMA/DECISIONES.md` (DEC-007), relevos en `08_SISTEMA_Y_AGENTES/handoffs/` y bitácoras para rescatar pendientes abiertos (`[VERIFICAR]`).
3. **Propuesta Estructurada y Rigor Metodológico:** Eleva el requerimiento a terminología académica y técnica formal (variables, normas APA 7, modelos UNAJMA, ISO/IEC 25010, TAM, Extreme Programming).
4. **Sugerencias Proactivas y Opciones Claras:** Plantea al tesista alternativas estructuradas y recomendaciones de élite, y sólo despacha la comisión formal cuando la directiva está calibrada.

### 3.1. Contrato de Comisión del Director (JSON Schema: `.claude/schemas/comision.schema.json`)
```text
TAREA: <Acción concreta, específica y acotada>
FASE: <Fx según ESTADO_TESIS.md>
SQUAD: <Squad A / B / C / D / E / F>
SUBAGENTE: <nombre-agente>
ENTRADAS: <Rutas exactas de archivos base o notas>
SALIDA ESPERADA: <Ruta y formato exacto del entregable>
RESTRICCIONES: <Reglas innegociables aplicables>
CRITERIO DE ÉXITO: <Métrica o condición objetiva de terminación>
```

### 3.2. Contrato de Handoff del Subagente (JSON Schema: `.claude/schemas/handoff.schema.json`)
Al concluir la tarea, el subagente deposita su informe en:  
`C:\MisInvestigaciones\obsidian_vault\08_SISTEMA_Y_AGENTES\handoffs\AAAA-MM-DD_<agente>_<tarea>.md` (máximo 300 palabras):
1. **Estado:** `completado` | `parcial` | `bloqueado`.
2. **Productos Generados:** Rutas de archivos creados o actualizados.
3. **Hallazgos Clave:** Resumen fáctico de los resultados.
4. **Pendientes / `[VERIFICAR]`:** Incertidumbres a corroborar con el tesista.
5. **Riesgos o Desalineaciones:** Conflictos detectados con la matriz o la constitución.
6. **Siguiente Acción Sugerida:** Próximo paso metodológico.

---

## 4. Compuertas de Calidad (Quality Gates)

- **QG-0 (Ecosistema):** Granja, 17 skills, 5 MCPs, hooks canónicos y reglas operativas.
- **QG-1 (Diagnóstico):** Auditoría de brechas (`PROYECTO_TESIS.docx` vs modelos UNAJMA).
- **QG-2 (Metodología):** Matriz de consistencia y operacionalización cerradas con 3 dimensiones (DEC-007).
- **QG-3 (Marco Teórico):** 100% citas verificadas con Zotero / DOI activo.
- **QG-4 (Software XP):** Sección 3.3 documentada con fidelidad 1:1 al código real de `syncova`.
- **QG-5 (Instrumentos):** Paquete de validación por expertos con $V \ge 0.80$ e $IVC \ge 0.80$.
- **QG-6 (Bioestadística):** Scripts reproducibles y control de calidad de datos listo.
- **QG-7 (Resultados):** Normalidad evaluada y contrastes inferenciales con datos de campo reales.
- **QG-8 (Discusión y Conclusiones):** Correspondencia 1:1 estricta con los objetivos.
- **QG-9 (Editorial):** DOCX final compilado con OpenXML desvinculado, 300 DPI y dictamen aprobatorio del jurado.
- **COMPUERTA SUPREMA:** Autorización formal del Tesista Humano.
