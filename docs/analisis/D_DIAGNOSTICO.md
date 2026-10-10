# INFORME DE DIAGNÓSTICO INTEGRAL (FASE D)
## Auditoría Estructural, de Orquestación, Permisos y Compatibilidad Multi-CLI
> **Proyecto:** SIVAC-THESIS-LAB — Granja de Agentes de Investigación Científica  
> **Universidad:** Universidad Nacional José María Arguedas (UNAJMA) — EPIS  
> **Autor / Tesista:** Bach. José Luis Quispe León | **Asesora:** Dra. Norma Lorena Catacora Flores  
> **Fecha:** 2026-10-09  
> **Arquitecto Evaluador:** Arquitecto Senior de Sistemas Multiagente Autónomos  

---

## 1. Lo que Funciona Excepcionalmente y se Conserva Intacto

Antes de detallar los hallazgos críticos, es fundamental reconocer los pilares del sistema que poseen un nivel de madurez y excelencia superior:

1. **Blindaje Metodológico DEC-007:** La Variable Dependiente está fijada de manera canónica en sus 3 dimensiones oficiales e inmutables (*Oportunidad de procesamiento*, *Consistencia documental*, *Satisfacción del usuario*). No existe desvío de constructo.
2. **Cero Invención Empírica (Regla Canónica 01):** El sistema resiste la tentación de simular datos. Los contrastes inferenciales de Wilcoxon y el Alfa de Cronbach se mantienen bajo marcadores formales `[Pendiente]`, esperando la recolección de campo real con la población censal ($N = n = 14$).
3. **Pipeline Quirúrgico OpenXML (`scripts/utilidades/docx_quirurgico.py`):** El ensamblado de Word no pasa por traductores genéricos. Inyecta ecuaciones nativas de Word `<m:oMath>`, tablas APA 7 de tres líneas horizontales y figuras a 300 DPI, eliminando fórmulas en celdas y signos de LaTeX.
4. **Cerebro en Obsidian (`C:\MisInvestigaciones\obsidian_vault`):** La estructura Zettelkasten / PARA / MOCs almacena 42 notas de relevo (handoffs), bitácoras por agente, y la única fuente de verdad: `00_SISTEMA/ESTADO_TESIS.md`.
5. **Calidad Académica Verificada:** El último borrador (`informe_final_v01.docx`) obtuvo dictamen aprobatorio de 18.38/20 en el simulador de jurado de la UNAJMA y 100% de consistencia biunívoca en sus 36 referencias en APA 7.

---

## 2. Matriz Maestra de Hallazgos y Diagnóstico

| ID | Hallazgo | Categoría | Grav. | Evidencia (Archivo:Línea) | Impacto en la Tesis | Recomendación / Corrección |
|---|---|---|---|---|---|---|
| **DIA-01** | **Invisibilidad de agentes en Factory Droid** | Compatibilidad Claude/Droid | 🔴 | Raíz del proyecto (falta `.factory/droids/`) | Droid no puede descubrir los 14 agentes en `/droids` ni delegarles con `Task(subagent_type: "<agente>")`. Se degrada a usar workers genéricos. | Implementar `scripts/sync_factory.py` que traduzca `.claude/agents/*.md` a `.factory/droids/*.md` con frontmatter adaptado. |
| **DIA-02** | **Skills de tesis no disponibles para Droid** | Skills / Compatibilidad | 🔴 | Falta enlace `.factory/skills/` | Las 21 skills especializadas de la tesis solo están en `.claude/skills/`. Droid no puede invocarlas automáticamente por su `description`. | Sincronizar `.factory/skills/` mediante Junction (`mklink /J`) o sincronización de carpetas desde `.claude/skills/`. |
| **DIA-03** | **Sobreasignación de privilegios shell (`Bash`/`PowerShell`)** | Permisos / Seguridad | 🟠 | `.claude/agents/*.md` (12 de 14 agentes) | Agentes de pura revisión o redacción (ej. `guardian-consistencia`, `jurado-revisor`) tienen acceso a consola. Riesgo de ejecución accidental o no controlada. | Restringir herramientas de shell solo a `director-general`, `maquetador-docx`, `analista-estadistico` y `analista-documental`. Los demás solo herramientas de archivo. |
| **DIA-04** | **Conflicto de contexto inicial (`CLAUDE.md` vs `AGENTS.md`)** | Duplicación de configuración | 🟠 | Raíz: `CLAUDE.md` (8 KB) y `AGENTS.md` (11 KB) | Ambos archivos se inyectan en el prompt inicial de Droid, consumiendo ~19 KB del presupuesto de 80 KB de instrucciones y duplicando reglas. | Mantener `CLAUDE.md` como canónico conciso y dejar `AGENTS.md` como un puente estructurado hacia `CLAUDE.md` y mapa de squads. |
| **DIA-05** | **Discrepancia de modelo declarado (`opus` vs `sonnet`)** | Arquitectura / Modelos | 🟡 | `AGENTS.md`: tabla sec. 2 (`opus`) vs `.claude/agents/*.md`: frontmatter (`sonnet`) | Confusión en la directiva de inferencia. En Droid puede causar asignaciones erróneas o consumo excesivo de créditos si no se unifica. | Normalizar a `model: inherit` en `.factory/droids/` para heredar el modelo activo o usar `sonnet` como estándar operativo. |
| **DIA-06** | **Pseudo-skills que son servidores MCP (`context7`)** | Skills / Estructura | 🟡 | `.claude/agents/ingeniero-sivac.md`: l. 11, `documentador-xp.md`: l. 13 | Se lista `context7` dentro de `skills: [...]` en el frontmatter, pero no existe la carpeta `.claude/skills/context7/SKILL.md`. Es un servidor MCP. | Remover `context7` del arreglo de `skills` y declararlo en `mcpServers: ["context7"]`. |
| **DIA-07** | **Servidores MCP caídos en Claude Code** | MCP / Rendimiento | 🟡 | `claude mcp list` (`Latted`, `open-design`) | Generan timeouts de 30 segundos en cada arranque de Claude Code, ralentizando el inicio de sesión. | Limpiar entradas huérfanas en la configuración de Claude Code. |
| **DIA-08** | **Falta de hooks de seguridad activos en Factory Droid** | Gobernanza / Seguridad | 🟠 | `.claude/settings.json` vs inexistente `.factory/hooks.json` | El hook `pretooluse_blocker.cjs` que protege `syncova` y `referencias/` solo protege a Claude Code. En Droid no está activo a nivel de proyecto. | Generar `.factory/hooks.json` apuntando a los mismos scripts `.claude/hooks/*.cjs` adaptando el exit code 2. |
| **DIA-09** | **Riesgo de ejecución monolítica del Agente GOD** | Orquestación | 🟠 | Sesiones históricas en bitácoras | El Director General tiende a editar código o redactar texto directamente cuando la tarea es pequeña, eludiendo a los subagentes. | Reforzar en la constitución el mandato de delegación y utilizar `Task` con subagentes especializados. |
| **DIA-10** | **Timeouts en automatización Word COM** | DOCX / Infraestructura | 🟡 | `scripts/utilidades/test_word_com_clean.py` | La llamada COM a Word puede bloquearse indefinidamente si Word abre diálogos modales invisibles de recuperación de archivos. | Asegurar timeouts en llamadas y manejo robusto de procesos con `kill_hung_word.py`. |
| **DIA-11** | **Dependencia de Zotero Desktop en segundo plano** | MCP / Bibliografía | 🟢 | `scripts/agentes/estado_granja.py`: l. 15 | Si Zotero no está abierto o el socket HTTP local está inactivo, las búsquedas de fuentes se bloquean. | Documentar en la guía operativa el prerrequisito de mantener Zotero abierto en segundo plano. |
| **DIA-12** | **Dispersión de scripts temporales de prueba en raíz y salidas** | Mantenibilidad | 🟢 | Raíz (`test_outline.docx`, etc.) y `salidas/` (`_tmp_auditoria/`, etc.) | Desorden en la raíz y carpetas de salida con artefactos de pruebas anteriores. | Agrupar y mover pruebas a `_archive/` o `salidas/_tmp/`. |

---

## 3. Síntesis Diagnóstica

La granja multiagente cuenta con una arquitectura teórica y metodológica impecable, pero sufre de una **brecha de integración técnica entre plataformas**. El sistema fue concebido exclusivamente para Claude Code, y Factory Droid ha venido operando en él de manera "adaptada", sin contar con sus archivos nativos (`.factory/droids/`, `.factory/skills/`, `.factory/hooks.json`, `.factory/mcp.json`).

El objetivo del Plan de Mejora (Fase E) no es reescribir la tesis ni cambiar la metodología DEC-007, sino **construir la capa de compatibilidad generada automatizada (`scripts/sync_factory.py`) que haga que Factory Droid y Claude Code compartan el 100% de los agentes, skills, hooks y MCPs de forma nativa y sin fricciones**.
