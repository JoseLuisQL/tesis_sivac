# MATRIZ MAESTRA DE LA GRANJA DE AGENTES — SIVAC-THESIS-LAB
> **Ecosistema Multi-Agente de Investigación Científica para el Informe Final de Tesis**  
> **Escuela Profesional de Ingeniería de Sistemas — Universidad Nacional José María Arguedas (UNAJMA)**  
> **Topología:** Hub-and-Spoke (Estrella Jerárquica Radial) | **Orquestador:** Agente GOD (`director-general`)

---

## 1. Topología del Sistema y Principio de Mando

```
                               ┌────────────────────────────────────────────────────────┐
                               │               TESISTA HUMANO (Investigador)            │
                               │        [Última Autoridad - Aprobaciones de Fase]       │
                               └───────────────────────────▲────────────────────────────┘
                                                           │ Aprobación / Feedback
                               ┌───────────────────────────▼────────────────────────────┐
                               │             AGENTE GOD / DIRECTOR GENERAL              │
                               │               (Sesión Principal / Lead)                │
                               │   - Orquestador Maestro de la Constitución (CLAUDE.md) │
                               │   - Gestor de Fases y Única Fuente de Verdad           │
                               │   - Enrutador Formal de Tareas a Squads Especializados │
                               │   - Supervisor de Quality Gates y Cero Alucinaciones   │
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
| **Hub Central** | `director-general` | Agente GOD / Orquestador Maestro | Claude 5 | Read, Write, Edit, Grep, Glob, Bash, PowerShell, Agent, Skill, Tasks | `academic-pipeline`, `matriz-consistencia`, `estructura-tesis-universidad` |
| **Squad A** | `investigador-bibliografico` | Búsqueda y síntesis sistemática | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `deep-research`, `zotero-busqueda-academica`, `apa7-es-tesis` |
| **Squad A** | `verificador-integridad` | Auditoría 1:1 y anti-alucinaciones | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `academic-paper` (citation-check), `deep-research` (fact-check) |
| **Squad B** | `guardian-consistencia` | Custodio isomórfico (3 dims DEC-007) | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `matriz-consistencia`, `estructura-tesis-universidad` |
| **Squad B** | `especialista-instrumentos` | Diseño psicométrico y juicio expertos | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `formato-instrumentos-validacion`, `validacion-psicometrica` |
| **Squad B** | `especialista-forms` | Formularios digitales y Apps Script | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `formato-instrumentos-validacion`, `validacion-psicometrica` |
| **Squad C** | `ingeniero-sivac` | Auditor de software (SOLO LECTURA) | opus | **Solo Lectura:** Read, Grep, Glob | `context7`, `extraccion-figuras-pdf-docx` |
| **Squad C** | `documentador-xp` | Redactor de sección 3.3 (XP, UML) | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `redaccion-academica-verificable`, `extraccion-figuras-pdf-docx` |
| **Squad D** | `analista-estadistico` | Bioestadístico y contrastes ($n=14$) | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `analisis-estadistico-avanzado`, `dataviz`, `xlsx` |
| **Squad E** | `analista-documental` | Desglose estructural de modelos UNAJMA | opus | Read, Grep, Glob, Bash, PowerShell | `docx`, `pdf`, `xlsx`, `estructura-tesis-universidad` |
| **Squad E** | `redactor-academico` | Redactor en prosa científica APA 7 | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `academic-paper`, `apa7-es-tesis`, `redaccion-academica-verificable` |
| **Squad E** | `maquetador-docx` | Compilador OpenXML desvinculado | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `tablas-quirurgicas-docx-apa7`, `referencias-nativas-docx-apa7`, `docx` |
| **Squad F** | `curador-cerebro` | Custodio de Obsidian (No destrucción) | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `protocolo-obsidian-handoff` |
| **Squad F** | `jurado-revisor` | Tribunal simulado UNAJMA (20 pts) | opus | Read, Write, Edit, Grep, Glob, Bash, PowerShell | `academic-paper-reviewer`, `matriz-consistencia` |

---

## 3. Protocolos de Comisión y Handoff

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
