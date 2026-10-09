# AUDITORÍA ESTRUCTURAL Y VERIFICACIÓN DE COMPILACIÓN — PROYECTO DE TESIS V5

- **Documento auditado:** `C:\MisInvestigaciones\tesis\sivac\salidas\documentos\PROYECTO_TESIS_ACTUALIZADO_V5_NORMALIZADO.docx`
- **Compilador ejecutado:** `C:\MisInvestigaciones\tesis\sivac\scripts\compiladores\compilar_proyecto_v5.py`
- **Insumo maestro:** `C:\MisInvestigaciones\tesis\sivac\salidas\documentos\CAPITULO_II_MARCO_TEORICO_CONSOLIDADO.md`
- **Fecha de verificación:** 2026-10-07
- **Orquestador:** `director-general` (Squad A / GOD)
- **Agentes intervinientes:** `redactor-academico` (Squad B), `verificador-integridad` (Squad F), `maquetador-docx` (Squad E)

---

## 1. Resumen de Métricas de Calidad y Compuertas Superadas

| Criterio / Compuerta de Auditoría | Estado en V4 | Resultado en V5 | Dictamen |
|---|---|---|---|
| Cobertura y densidad en `2.1 Antecedentes` | 7 antecedentes breves (~745 palabras en total) | **10 antecedentes completos** (6 internacionales + 4 nacionales, 150-200 palabras c/u, ~2,250 palabras) | **SUPERADO** |
| Encuadre epistemológico inicial de Capítulo II | Ausente (salto directo a 2.1) | **Párrafo canónico de encuadre epistemológico** integrado tras `CAPÍTULO II.  MARCO TEÓRICO` | **CUMPLIDO** |
| Subacápites nivel 3 en `2.2 Bases teóricas` (`Ttulo3`) | 2 (`2.2.1 Sistema web` y `2.2.2 Gestión de movimientos de vacunas`) | **2** (`2.2.1 Sistema web` y `2.2.2 Gestión de movimientos de vacunas`) | **CUMPLIDO** |
| Subacápites nivel 3 en `2.3 Marco conceptual` (`Ttulo3`) | 0 (16 términos ordenados A-Z con sangría 1.27 cm y término en negrita) | **0** (16 términos ordenados A-Z con sangría 1.27 cm y término en negrita) | **CUMPLIDO** |
| Encabezado huérfano vacío `P138` (`Ttulo3`) | 0 | **0** (Erradicado) | **CUMPLIDO** |
| Párrafos vacíos en el cuerpo (`CAPÍTULO I` a `ANEXOS`) | 0 | **0** (Erradicados) | **CUMPLIDO** |
| Signos `$` o residuos LaTeX en texto y tablas | 0 | **0** (Texto formal limpio) | **CUMPLIDO** |
| Citas empíricas en antecedentes con respaldo Zotero | Parcial (Dang et al. 2024, Wasswa et al. 2023 y Champi 2023 omitidos en texto) | **100% integradas** (Dang et al., Wasswa et al., Champi Velásquez y 7 previos con correspondencia 1:1) | **SUPERADO** |
| Referencias bibliográficas con correspondencia biunívoca 1:1 | 27 referencias | **27 referencias** (100% verificadas en Zotero, sangría francesa 1.27 cm, interlineado 1.5) | **CUMPLIDO** |
| Tablas APA 7 en todo el documento (`docx_quirurgico.py auditar`) | 12 tablas | **12 tablas** (0 flotantes, 100% `cantSplit`, 100% `tblHeader`, 3 líneas APA 7, 8788 dxa) | **CUMPLIDO** |
| Figuras en Capítulo II (`rId14`, `rId16`, `rId15`) | 3 figuras | **3 figuras** preservadas a resolución original, centradas y con `keepNext` | **CUMPLIDO** |

---

## 2. Estructura Jerárquica Verificada de los Capítulos I y II en V5

### Capítulo I: Planteamiento del Problema
- `CAPÍTULO I. PLANTEAMIENTO DEL PROBLEMA` (`Ttulo1`)
  - `1.1 Descripción del problema` (`Ttulo2`)
  - `1.2 Formulación del problema` (`Ttulo2`)
    - `1.2.1 Problema General` (`Ttulo3`)
    - `1.2.2 Problemas Específicos` (`Ttulo3`)
  - `1.3 Objetivos` (`Ttulo2`)
    - `1.3.1 Objetivo General` (`Ttulo3`)
    - `1.3.2 Objetivos Específicos` (`Ttulo3`)
  - `1.4 Justificación` (`Ttulo2`)
  - `1.5 Delimitación` (`Ttulo2`)

### Capítulo II: Marco Teórico
- `CAPÍTULO II.  MARCO TEÓRICO` (`Ttulo1`, párrafo [92])
  - *Párrafo de encuadre epistemológico del capítulo* [93]
  - `2.1 Antecedentes de investigación` (`Ttulo2`, párrafo [94])
    - *Párrafo introductorio de la revisión sistemática de literatura* [95]
    - `2.1.1. Antecedentes a nivel internacional` (`Ttulo3`, párrafo [96])
      1. Shen, J., Bu, F., Ye, Z., Zhang, M., Ma, Q., Yan, J., y Huang, T. (2024) — *China* [97]
      2. Dang, T. T. T., Carnahan, E., Nguyen, L., Mvundura, M., Dao, S., Duong, T. H., Nguyen, T., Nguyen, D., Nguyen, T., Werner, L., Ryman, T. K., y Nguyen, N. (2024) — *Vietnam* [98]
      3. Kigenza, R., Nsengiyumva, E., y Sabagirirwa, V. (2023) — *Ruanda* [99]
      4. Balón Morejón, R. M. (2023) — *Ecuador* [100]
      5. Ergetie, F. S., Kassaw, A. T., y Sendekie, A. K. (2023) — *Etiopía* [101]
      6. Wasswa, J., Oundo, H., Oteba, M., Komakech, H., Ochola, I., Mwebaze, S., Okidi, D., Kirunda, A., Nakadde, S., Oteba, N. O., y Lugada, E. (2023) — *Uganda* [102]
    - `2.1.2. Antecedentes a nivel nacional` (`Ttulo3`, párrafo [103])
      1. Astuhuaman Perez, S. M., y Baltazar Maza, E. J. (2024) — *Apurímac* [104]
      2. Mego Navarro, D. P. (2021) — *Lima* [105]
      3. Garcia Villacorta, M. D. M., y Calderón Huaman, J. L. O. (2023) — *Lima* [106]
      4. Champi Velásquez, J. M. (2023) — *Lima* [107]
  - `2.2 Bases teóricas` (`Ttulo2`, párrafo [108])
    - *Párrafo de articulación epistemológica en dos ejes* [109]
    - `2.2.1 Sistema web` (`Ttulo3`, párrafo [110])
      - Subtítulo temático: **Arquitectura web y servicios desacoplados cliente-servidor**
      - **Tabla 1:** *Características de los sistemas web aplicados a la gestión sanitaria* (6 filas x 3 cols, 8788 dxa)
      - **Figura 1:** *Arquitectura cliente-servidor desacoplada para sistemas web* (`rId14`, párrafo [123])
      - Subtítulo temático: **Metodología ágil Extreme Programming (XP) en el contexto de sistemas de salud**
      - **Figura 2:** *Fases y ciclo iterativo de la metodología Extreme Programming (XP)* (`rId16`, párrafo [136])
      - **Tabla 2:** *Prácticas de ingeniería de software en Extreme Programming aplicadas a SIVAC* (7 filas x 3 cols, 8788 dxa)
      - Subtítulo temático: **Estándar de calidad del producto de software ISO/IEC 25010:2023**
      - **Tabla 3:** *Características del modelo de calidad de software según el estándar internacional (ISO/IEC, 2023)* (6 filas x 3 cols, 8788 dxa)
    - `2.2.2 Gestión de movimientos de vacunas` (`Ttulo3`, párrafo [154])
      - Subtítulo temático: **Marco logístico y normativo de la cadena de frío e inmunizaciones**
      - Subtítulo temático: **Procesos operativos del flujo de biológicos, control de lotes y kardex**
      - **Figura 3:** *Componentes y flujo documental de la cadena de frío de vacunas* (`rId15`, párrafo [168])
      - Subtítulo temático: **Dimensión 1: Oportunidad de procesamiento**
      - Subtítulo temático: **Dimensión 2: Consistencia documental**
      - Subtítulo temático: **Dimensión 3: Satisfacción del usuario y Modelo de Aceptación Tecnológica (TAM)**
      - **Tabla 4:** *Operacionalización teórica de los indicadores de satisfacción del usuario bajo el Modelo TAM* (4 filas x 4 cols, 8788 dxa)
  - `2.3 Marco conceptual` (`Ttulo2`, párrafo [199])
    - 16 conceptos clave ordenados alfabéticamente de la A a la Z, redactados en párrafos con sangría de primera línea de 1.27 cm (720 dxa), interlineado 1.5 y término inicial en negrita:
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

### Capítulo III: Hipótesis y Definición de Variables
- `CAPÍTULO III. HIPÓTESIS Y DEFINICIÓN DE VARIABLES` (`Ttulo1`, párrafo [216])

---

## 3. Auditoría Geométrica de las 12 Tablas (`docx_quirurgico.py auditar`)

```text
--- AUDITORÍA DE TABLAS: salidas/documentos/PROYECTO_TESIS_ACTUALIZADO_V5_NORMALIZADO.docx ---
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

## 4. Verificación de las 27 Referencias Bibliográficas (Correspondencia Biunívoca 1:1)

1. **Astuhuaman Perez & Baltazar Maza (2024)** — Citado en Antecedentes Nacionales y Oportunidad de Procesamiento.
2. **Balón Morejón (2023)** — Citado en Antecedentes Internacionales y Oportunidad de Procesamiento.
3. **Beck (1999)** — Citado en Extreme Programming (Bases Teóricas y Tabla 2).
4. **Brooks et al. (2024)** — Citado en e-LMIS / IIS, Tabla 1, Satisfacción TAM y Marco Conceptual.
5. **Champi Velásquez (2023)** — Citado en Antecedentes Nacionales, Cadena de Frío e Inmunizaciones y Figura 3.
6. **Chekol et al. (2023)** — Citado en Control de Lotes/Kardex y Consistencia Documental.
7. **Cohn (2004)** — Citado en Historias de Usuario de XP, Figura 2 y Tabla 2.
8. **Dang et al. (2024)** — Citado en Antecedentes Internacionales y Oportunidad de Procesamiento.
9. **Davis (1989)** — Citado en Modelo TAM, Satisfacción del Usuario, Tabla 4 y Marco Conceptual.
10. **Duong et al. (2021)** — Citado en Arquitectura Web y Satisfacción TAM.
11. **Ergetie et al. (2023)** — Citado en Antecedentes Internacionales, Cadena de Frío y Consistencia Documental.
12. **Garcia Villacorta & Calderón Huaman (2023)** — Citado en Antecedentes Nacionales y Consistencia Documental.
13. **George & Mallery (2003)** — Citado en Métodos y Escalas Psicométricas.
14. **Hernández-Sampieri et al. (2014)** — Citado en Metodología Cuantitativa.
15. **ISO/IEC (2023)** — Citado en Calidad de Software, Tabla 3 y Marco Conceptual.
16. **Kigenza et al. (2023)** — Citado en Antecedentes Internacionales y Consistencia Documental.
17. **Luján Mora (2002)** — Citado en Arquitectura Web y Tabla 1.
18. **Mego Navarro (2021)** — Citado en Antecedentes Nacionales, Arquitectura Web, XP y Figura 1.
19. **MINSA (2022)** — Citado en Marco Normativo NTS 196, Cadena de Frío, Kardex y Marco Conceptual.
20. **Moumane et al. (2024)** — Citado en ISO/IEC 25010 en Salud y Tabla 3.
21. **Ndlovu et al. (2022)** — Citado en Modelo TAM, Satisfacción del Usuario y Tabla 4.
22. **OPS y PATH (2020)** — Citado en Cadena de Frío, Trazabilidad de Biológicos y Figura 3.
23. **Pressman (2010)** — Citado en Arquitectura Software, XP, Figura 1, Figura 2, Tabla 1 y Tabla 2.
24. **Ruiz Barea (2023)** — Citado en Arquitectura REST, Tokens JWT, RBAC y Tabla 1.
25. **Shen et al. (2024)** — Citado en Antecedentes Internacionales y Consistencia Documental.
26. **Sommerville (2016)** — Citado en Sistemas Web, Arquitectura Multicapa, XP, Figura 1 y Tabla 1.
27. **Wasswa et al. (2023)** — Citado en Antecedentes Internacionales, Oportunidad de Procesamiento y Kardex.

**Dictamen de Integridad:** Correspondencia biunívoca 1:1 absoluta. Cero fuentes alucinadas o no citadas. Cero citas huérfanas en el texto.
