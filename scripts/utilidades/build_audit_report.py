# -*- coding: utf-8 -*-
import os

path = "salidas/documentos/AUDITORIA_CAP1_CAP2_ESTRUCTURA_Y_CITAS.md"

content = []

content.append("""# INFORME DE AUDITORÍA TÉCNICA Y DOCUMENTAL: CAPÍTULOS I Y II
**Documento Auditado:** `salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.docx`  
**Fase de la Granja:** F3 - Diagnóstico, Estructura y Verificación Bibliográfica
**Squad Responsable:** Squad A (Diagnóstico e Ingesta) / Squad E (Redacción, Estilo y Maquetación Editorial)  
**Agente Auditor:** `analista-documental`  
**Fecha de Emisión:** 2026-10-07  
**Estado:** COMPLETADO CON OBSERVACIONES CRÍTICAS

---

## 1. RESUMEN EJECUTIVO Y HALLAZGOS CRÍTICOS

El presente informe constituye la auditoría exhaustiva, fáctica, métrica y epistémica de los **Capítulos I (Planteamiento del Problema)** y **II (Marco Teórico y Antecedentes)** del documento base normalizado de la tesis SIVAC (`PROYECTO_TESIS_ACTUALIZADO_V3_NORMALIZADO.docx`).

La evaluación se realizó contrastando el manuscrito contra:
1. Las directivas de la **Constitución Operativa SIVAC (`CLAUDE.md`)** y las reglas canónicas de estilo académico (`03_estilo_academico_apa7.md`) y metodología (`02_metodologia_dec007.md`).
2. La **Matriz de Consistencia Metodológica Definitiva (`MATRIZ_CONSISTENCIA_DEFINITIVA.md`)**.
3. El **Catálogo Maestro de Fuentes Bibliográficas Zotero SIVAC (26 referencias verificadas)**.
4. El patrón documental de tesis laureadas de la EPIS-UNAJMA (**Jhon 2026**, 223 p., y **Fany 2024**, 106 p.).

### Cuadro de Hallazgos Críticos:
1. **Intrusión Temática de Inteligencia Artificial (Deriva Metodológica):** Se detectó la inclusión de un acápite innecesario `2.2.6 Inteligencia artificial` (P139 a P142) que cita a **Alhazmi et al. (2024)**. SIVAC es un sistema web transaccional desarrollado con Extreme Programming (XP) y evaluado bajo ISO/IEC 25010:2023; no implementa componentes de inteligencia artificial. Esta sección desvirtúa la coherencia con DEC-007.
2. **Cita No Catalogada (Riesgo de Alucinación Bibliográfica):** La cita **Alhazmi et al. (2024)** en P141 **NO existe en el Catálogo Maestro de Fuentes Zotero SIVAC ni en la colección institucional**.
3. **Cita Comercial No Académica en Nota de Figura:** En la Nota de Figura 3 (P241) se cita una URL de un blog comercial: `"Por SINNAPS, 2022, Sinnaps (https://www.sinnaps.com/...)"`. El estándar UNAJMA exige fundamentación teórica en obras seminales o normativas (Beck, 1999; Pressman, 2010).
4. **Cita con Fecha Errónea ("s. f."):** En P169 se cita a la `Organización Panamericana de la Salud y PATH (s. f.)` cuando la fuente catalogada oficial es **OPS & PATH (2020)** (`@opspath2020`).
5. **Hiper-fragmentación Estructural en Bases Teóricas (2.2):** Se registran **25 subacápites decimales de nivel 3** (`2.2.1` al `2.2.25`). Múltiples secciones contienen un único párrafo de entre 25 y 45 palabras (ej. 2.2.11 PNI: 36 palabras; 2.2.16 Lote: 31 palabras; 2.2.18 Kardex: 30 palabras; 2.2.19 Movimiento: 36 palabras). Esto fragmenta el discurso científico, asemejándose a un diccionario disperso.
6. **Hiper-fragmentación y Saturación del Índice en Marco Conceptual (2.3):** Se han generado **20 subencabezados Heading 3 decimales** (`2.3.1` al `2.3.20`), saturando la Tabla de Contenidos (Índice General) con entradas de un solo párrafo breve (16 a 32 palabras). Asimismo, se duplica casi el 70% de los términos ya expuestos en 2.2. En UNAJMA (Jhon 2026), el marco conceptual es una sección continua con términos en negrita sin numeración decimal.
7. **Anomalías OpenXML y Párrafos Vacíos:** Se detectó un encabezado huérfano vacío en P138 (`Heading 3` sin texto) y **25 párrafos vacíos (`0 palabras`)** introducidos como espaciadores verticales artificiales, lo cual altera el renderizado y las compuertas de inspección visual.
""")

with open(path, "w", encoding="utf-8") as f:
    f.write("".join(content))
print("Seccion 1 escrita")
