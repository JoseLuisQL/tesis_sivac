---
description: Protocolo de interacción Hub-and-Spoke, comisiones, handoffs y compuertas de calidad
---

# REGLA CANÓNICA 04: PROTOCOLO DE AGENTES, COMISIONES Y QUALITY GATES

## 1. Topología Jerárquica Hub-and-Spoke
- **Director General (Agente GOD):** Sesión principal de Claude Code. Único orquestador, administrador de la Constitución (`CLAUDE.md`) y la matriz de asignaciones (`AGENTS.md`).
- **Restricción Técnica Cardinal:** En Claude Code los subagentes no pueden invocar otros subagentes. Todo flujo de delegación es estrictamente radial: `Director General` $\longleftrightarrow$ `Subagente Especialista`.
- **Aprobación del Tesista Humano:** Ningún capítulo, instrumento o sección definitiva se integra en el documento oficial sin la revisión y aprobación expresa del tesista.

## 2. Contrato de Comisión del Director General (Director -> Subagente)
Toda asignación a un subagente debe emitirse con el siguiente formato estructurado:
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

## 3. Contrato de Handoff del Subagente (Subagente -> Director)
Todo subagente genera al concluir su nota de relevo en `08_SISTEMA_Y_AGENTES/handoffs/AAAA-MM-DD_<agente>_<tarea>.md` (máximo 300 palabras):
1. **Estado:** `completado` | `parcial` | `bloqueado`.
2. **Productos Generados:** Rutas exactas de archivos creados o actualizados.
3. **Hallazgos Clave:** Resumen fáctico de los resultados o evidencia.
4. **Pendientes / `[VERIFICAR]`:** Puntos de incertidumbre que requieren confirmación del tesista o auditoría bibliográfica.
5. **Riesgos o Desalineaciones:** Conflictos detectados con la matriz de consistencia o la constitución.
6. **Siguiente Acción Sugerida:** Próximo paso lógico en el flujo metodológico.

## 4. Bitácoras Individuales
- Cada subagente actualiza su bitácora histórica en `08_SISTEMA_Y_AGENTES/bitacoras/<agente>.md`.
- El Director General actualiza `00_SISTEMA/ESTADO_TESIS.md` como la **Única Fuente de Verdad**.

## 5. Compuertas de Calidad (Quality Gates)
- **QG-0:** Ecosistema, 17 skills, 5 MCPs, hooks canónicos y reglas operativas.
- **QG-1:** Diagnóstico y auditoría de brechas (`PROYECTO_TESIS.docx` vs modelos UNAJMA).
- **QG-2:** Matriz de consistencia y operacionalización cerradas con las 3 dimensiones (DEC-007).
- **QG-3:** Marco teórico y antecedentes con 100% de citas verificadas.
- **QG-4:** Sección 3.3 (Extreme Programming) documentada con fidelidad 1:1 al código real de `syncova`.
- **QG-5:** Paquete de validación por expertos con $V \ge 0.80$ e $IVC \ge 0.80$.
- **QG-6:** Bioestadística: scripts reproducibles y control de calidad de datos listo.
- **QG-7:** Resultados: normalidad evaluada y contrastes inferenciales con datos de campo reales.
- **QG-8:** Discusión y conclusiones con correspondencia 1:1 estricta con los objetivos.
- **QG-9:** Documento DOCX final compilado con OpenXML desvinculado, 300 DPI y dictamen aprobatorio del jurado.
- **COMPUERTA SUPREMA:** Autorización formal del Tesista Humano.
