# AUDITORÍA ESTRUCTURAL Y VERIFICACIÓN DE COMPILACIÓN — PROYECTO DE TESIS V4

- **Documento auditado:** `C:\MisInvestigaciones\tesis\sivac\salidas\documentos\PROYECTO_TESIS_ACTUALIZADO_V4_NORMALIZADO.docx`
- **Compilador ejecutado:** `C:\MisInvestigaciones\tesis\sivac\scripts\compiladores\compilar_proyecto_v4.py`
- **Insumo maestro:** `C:\MisInvestigaciones\tesis\sivac\salidas\documentos\PROPUESTA_BASES_TEORICAS_Y_MARCO_CONCEPTUAL_CAP2.md`
- **Fecha de verificación:** 2026-10-07
- **Agente:** `maquetador-docx` (Squad E)

---

## 1. Resumen de Métricas de Calidad y Compuertas Superadas

| Criterio / Compuerta de Auditoría | Estado en V3 | Resultado en V4 | Dictamen |
|---|---|---|---|
| Subacápites nivel 3 en `2.2 Bases teóricas` (`Ttulo3`) | 25 (`2.2.1` a `2.2.25`) + 1 huérfano (`P138`) | **2** (`2.2.1 Sistema web` y `2.2.2 Gestión de movimientos de vacunas`) | **CUMPLIDO** |
| Subacápites nivel 3 en `2.3 Marco conceptual` (`Ttulo3`) | 20 (`2.3.1` a `2.3.20`) | **0** (16 términos ordenados A-Z con sangría 1.27 cm y término en negrita) | **CUMPLIDO** |
| Encabezado huérfano vacío `P138` (`Ttulo3`) | Presente (1) | **0** (Erradicado) | **CUMPLIDO** |
| Párrafos vacíos en el cuerpo (`CAPÍTULO I` a `ANEXOS`) | Múltiples | **0** | **CUMPLIDO** |
| Signos `$` o residuos LaTeX en texto y tablas | 0 | **0** | **CUMPLIDO** |
| Etiqueta residual `(según corresponda)` en `1.2.2` y TOC | Presente | **0** (`1.2.2 Problemas Específicos`) | **CUMPLIDO** |
| Citas desalineadas (`OPS y PATH, s. f.`, `Ndlovu et al., 2021`) | Presentes | **0** (Normalizadas a `OPS y PATH, 2020` y `Ndlovu et al., 2022`) | **CUMPLIDO** |
| Referencias bibliográficas con correspondencia biunívoca 1:1 | 35 (con 8 no citadas / comerciales y 1 sin año) | **27** (100% verificadas en Zotero, sangría francesa 1.27 cm, interlineado 1.5) | **CUMPLIDO** |
| Tablas APA 7 en todo el documento (`docx_quirurgico.py auditar`) | 12 tablas | **12 tablas** (0 flotantes, 100% `cantSplit`, 100% `tblHeader`, 3 líneas APA 7) | **CUMPLIDO** |
| Figuras en Capítulo II (`rId14`, `rId16`, `rId15`) | 3 figuras | **3 figuras** preservadas a resolución original, centradas y con `keepNext` | **CUMPLIDO** |

---

## 2. Estructura Jerárquica Verificada de los Capítulos I y II

### Capítulo I: Planteamiento del Problema
- `CAPÍTULO I. PLANTEAMIENTO DEL PROBLEMA` (`Ttulo1`)
  - `1.1 Descripción del problema` (`Ttulo2`)
  - `1.2 Formulación del problema` (`Ttulo2`)
    - `1.2.1 Problema General` (`Ttulo3`)
    - `1.2.2 Problemas Específicos` (`Ttulo3` — etiqueta `(según corresponda)` eliminada tanto en el cuerpo como en el Índice General)
  - `1.3 Objetivos` (`Ttulo2`)
    - `1.3.1 Objetivo General` (`Ttulo3`)
    - `1.3.2 Objetivos Específicos` (`Ttulo3`)
  - `1.4 Justificación` (`Ttulo2`)
  - `1.5 Delimitación` (`Ttulo2`)

### Capítulo II: Marco Teórico
- `CAPÍTULO II. MARCO TEÓRICO` (`Ttulo1`)
  - `2.1 Antecedentes de investigación` (`Ttulo2`)
    - `2.1.1. Antecedentes a nivel internacional` (`Ttulo3`)
    - `2.1.2. Antecedentes a nivel nacional` (`Ttulo3`)
  - `2.2 Bases teóricas` (`Ttulo2`)
    - `2.2.1 Sistema web` (`Ttulo3`)
      - Subtítulo temático: **Arquitectura web y servicios desacoplados cliente-servidor**
      - **Tabla 1:** *Características de los sistemas web aplicados a la gestión sanitaria* (6 filas x 3 columnas, 8788 dxa)
      - **Figura 1:** *Arquitectura cliente-servidor desacoplada para sistemas web* (`rId14`)
      - Subtítulo temático: **Metodología ágil Extreme Programming (XP) en el contexto de sistemas de salud**
      - **Figura 2:** *Fases y ciclo iterativo de la metodología Extreme Programming (XP)* (`rId16`)
      - **Tabla 2:** *Prácticas de ingeniería de software en Extreme Programming aplicadas a SIVAC* (7 filas x 3 columnas, 8788 dxa)
      - Subtítulo temático: **Estándar de calidad del producto de software ISO/IEC 25010:2023**
      - **Tabla 3:** *Características del modelo de calidad de software según el estándar internacional (ISO/IEC, 2023)* (6 filas x 3 columnas, 8788 dxa)
    - `2.2.2 Gestión de movimientos de vacunas` (`Ttulo3`)
      - Subtítulo temático: **Marco logístico y normativo de la cadena de frío e inmunizaciones**
      - Subtítulo temático: **Procesos operativos del flujo de biológicos, control de lotes y kardex**
      - **Figura 3:** *Componentes y flujo documental de la cadena de frío de vacunas* (`rId15`)
      - Subtítulo temático: **Dimensión 1: Oportunidad de procesamiento**
      - Subtítulo temático: **Dimensión 2: Consistencia documental**
      - Subtítulo temático: **Dimensión 3: Satisfacción del usuario y Modelo de Aceptación Tecnológica (TAM)**
      - **Tabla 4:** *Operacionalización teórica de los indicadores de satisfacción del usuario bajo el Modelo TAM* (4 filas x 4 columnas, 8788 dxa)
  - `2.3 Marco conceptual` (`Ttulo2`)
    - 16 conceptos clave ordenados alfabéticamente de la A a la Z, redactados en párrafos con sangría de primera línea de 1.27 cm (720 dxa), interlineado 1.5 y término inicial en negrita seguido de punto:
      1. **Aceptación del proceso.**
      2. **Cadena de frío.**
      3. **Centro de acopio de vacunas.**
      4. **Concordancia programada vs entregada.**
      5. **Consistencia documental.**
      6. **Extreme Programming (XP).**
      7. **Gestión de movimientos de vacunas.**
      8. **Inventario de vacunas.**
      9. **Kardex de biológicos.**
      10. **Lote de vacunas.**
      11. **Movimiento de vacunas.**
      12. **Oportunidad de procesamiento.**
      13. **Registros sin discrepancias.**
      14. **Sistema de información de inmunización.**
      15. **Sistema web SIVAC.**
      16. **Utilidad percibida.**

---

## 3. Auditoría Geométrica de las 12 Tablas (`docx_quirurgico.py auditar`)

```text
Total de tablas: 12
  [Tabla 1] 6 filas x 3 cols | Ancho: 8788 dxa | Flotante: False | cantSplit: 6/6 | Header: True
  [Tabla 2] 7 filas x 3 cols | Ancho: 8788 dxa | Flotante: False | cantSplit: 7/7 | Header: True
  [Tabla 3] 6 filas x 3 cols | Ancho: 8788 dxa | Flotante: False | cantSplit: 6/6 | Header: True
  [Tabla 4] 4 filas x 4 cols | Ancho: 8788 dxa | Flotante: False | cantSplit: 4/4 | Header: True
  [Tabla 5] 8 filas x 5 cols | Ancho: 8788 dxa | Flotante: False | cantSplit: 8/8 | Header: True
  [Tabla 6] 4 filas x 2 cols | Ancho: 9072 dxa | Flotante: False | cantSplit: 4/4 | Header: True
  [Tabla 7] 4 filas x 3 cols | Ancho: 8788 dxa | Flotante: False | cantSplit: 4/4 | Header: True
  [Tabla 8] 4 filas x 3 cols | Ancho: 8788 dxa | Flotante: False | cantSplit: 4/4 | Header: True
  [Tabla 9] 6 filas x 2 cols | Ancho: 9072 dxa | Flotante: False | cantSplit: 6/6 | Header: True
  [Tabla 10] 10 filas x 27 cols | Ancho: 14050 dxa | Flotante: False | cantSplit: 10/10 | Header: True
  [Tabla 11] 21 filas x 5 cols | Ancho: 8700 dxa | Flotante: False | cantSplit: 21/21 | Header: True
  [Tabla 12] 5 filas x 7 cols | Ancho: 14000 dxa | Flotante: False | cantSplit: 5/5 | Header: True
[✓] Todas las tablas cumplen con las directivas de contención y flujo natural.
```

---

## 4. Verificación de las 27 Referencias Bibliográficas (Correspondencia 1:1)

Las 27 referencias en la sección `Referencia Bibliográfica` presentan estilo `Bibliografa`, sangría francesa de 1.27 cm (`w:left="720" w:hanging="720"`), interlineado 1.5 (`w:line="360"`), espaciado posterior de 6 pt (`w:after="120"`), orden alfabético estricto (Astuhuaman Perez & Baltazar Maza, 2024 $\rightarrow$ Wasswa et al., 2023) y correspondencia biunívoca 1:1 con las citas del cuerpo del documento. Se erradicaron por completo las 8 referencias no citadas o comerciales detectadas en la versión anterior (`Alhazmi et al., 2024`, `Arisholm et al., 2007`, `Cortés Rojas, 2024`, `De la Torre Llorente et al., 2020`, `Jain & Arora, 2025`, `Naik & Raj, 2023`, `Pérez Peña & Ramos Jurado, 2021`, `Romero Onofre, 2016`) y se incorporó `Davis (1989)` con DOI verificado.
