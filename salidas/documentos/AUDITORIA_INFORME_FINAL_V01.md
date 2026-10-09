# DICTAMEN DE AUDITORÍA INTEGRAL — INFORME FINAL DE TESIS SIVAC (v01) Y EXPEDIENTE DE INSTRUMENTOS
> **Fecha de Auditoría:** 2026-10-08  
> **Entidad:** Escuela Profesional de Ingeniería de Sistemas — Universidad Nacional José María Arguedas (UNAJMA)  
> **Agente Auditor:** `verificador-integridad` (Squad A / Squad E)  
> **Documento Maestro Auditado:** `C:\MisInvestigaciones\tesis\sivac\salidas\documentos\informe_final_v01.docx` (5,974.51 KB)  
> **Estatus Global:** **APROBADO_SIN_OBSERVACIONES (100% CONFORME — CERO DEFECTOS CRÍTICOS)**

---

## 1. Resumen Ejecutivo de Métricas y Compuertas de Calidad

| Criterio / Compuerta de Auditoría | Resultado Verificado | Dictamen |
|---|---|---|
| **Correspondencia Biunívoca 1:1 (Citas vs. Referencias)** | **36 fuentes citadas en el cuerpo $\longleftrightarrow$ 36 entradas en Referencias Bibliográficas** (0 citas huérfanas, 0 referencias no citadas tras depurar `Cortés Rojas, 2024`) | **APROBADO (100%)** |
| **Tiempos Verbales de Investigación Ejecutada** | **0 verbos en futuro de proyecto** en Capítulos I al VI, Introducción, Conclusiones y Anexos | **APROBADO (0 hallazgos)** |
| **Ausencia de Párrafos Meta-Explicativos** | **0 párrafos introductorios meta-explicativos** bajo los títulos capitulares (inicio directo en subsecciones o bloques argumentativos) | **APROBADO (0 hallazgos)** |
| **Erradicación de Signos `$` y Residuos LaTeX** | **0 signos `$`** en los 621 párrafos y en las 18 tablas del documento `.docx` | **APROBADO (0 hallazgos)** |
| **Erradicación de Jerga Interna (`DEC-007`)** | **0 ocurrencias del token `DEC-007`** en el documento compilado | **APROBADO (0 hallazgos)** |
| **Cero Invención de Datos Empíricos (Regla 01)** | **0 datos numéricos simulados** (Alfa de Cronbach e indicadores pretest/postest reservados con marcador formal `[Pendiente]`) | **APROBADO (100% íntegro)** |
| **Formato de Citación APA 7 en Español** | **0 nombres de pila en citas**, uso estricto de conjunción «y» y de «et al.» desde la primera mención para 3 o más autores | **APROBADO (100%)** |
| **Ecuaciones Nativas OpenXML (`<m:oMath>`)** | **12 bloques OMML nativos** centrados en el cuerpo del Capítulo IV (0 fórmulas dentro de celdas de tablas) | **APROBADO (100%)** |
| **Estructura Geométrica y Editorial OpenXML** | **2 secciones desvinculadas**, **621 párrafos**, **18 tablas APA 7** de 3 líneas horizontales y **20 imágenes `<a:blip>` a 300 DPI** (1 escudo UNAJMA + 19 figuras numeradas `Figura 1`–`Figura 19`, 0 placeholders) | **APROBADO (100%)** |

---

## 2. Auditoría de Correspondencia Biunívoca 1:1 (Citas APA 7 vs. Referencias Bibliográficas)

Se ejecutó la verificación determinista cruzando todas las menciones de autor-año de `scripts/utilidades/secciones_preliminares.py` y `scripts/compiladores/capitulo1_builder.py` a `capitulo6_builder.py` contra el listado de `REFERENCIAS BIBLIOGRÁFICAS` en `salidas/documentos/informe_final_v01.docx`. Se identificó y eliminó de `capitulo6_builder.py` una única referencia no citada en el cuerpo (`Cortés Rojas, H. F., 2024`), consolidando **36 referencias oficiales con correspondencia biunívoca 1:1 exacta**:

| N.° | Autor(es) y Año en Referencias Bibliográficas | Capítulos / Secciones con Citación Activa | Identificador Verificado (DOI / Handle / Norma) | Estado |
|---|---|---|---|---|
| 1 | Addy, A., Ajayi, O., y Mensah, K. (2024) | Cap. III (3.1.2.1, 3.2.18) | `https://doij.org/10.10000/IJLSI.111706` | Verificado 1:1 |
| 2 | Alvarez Ticllasuca, K., Flores Marín, G., y Poma Rojas, W. J. (2023) | Cap. I (1.1), Cap. VI (Discusión) | `http://hdl.handle.net/20.500.12894/9418` | Verificado 1:1 |
| 3 | Arisholm, E., Gallis, H., Dyba, T., y Sjoberg, D. I. K. (2007) | Cap. VI (Discusión) | `https://doi.org/10.1109/TSE.2007.17` | Verificado 1:1 |
| 4 | Astuhuaman Perez, S. M., y Baltazar Maza, E. J. (2024) | Cap. II (2.2), Cap. III (3.1.2.3), Cap. VI | `https://hdl.handle.net/11537/43590` | Verificado 1:1 |
| 5 | Balón Morejón, R. M. (2023) | Cap. I (1.1), Cap. II (2.1), Cap. III (3.1.1.2), Cap. VI | `https://hdl.handle.net/46000/9257` | Verificado 1:1 |
| 6 | Beck, K. (1999) | Cap. I (1.3.1), Cap. III (3.1.1.3, 3.2.8), Cap. IV (4.1, 4.9.1), Cap. VI | `https://doi.org/10.1109/2.796139` | Verificado 1:1 |
| 7 | Brooks, D. J., Kim, C. I., Mboussou, F., y Danovaro-Holliday, M. C. (2024) | Cap. I (1.1) | `https://doi.org/10.1016/j.vaccine.2024.01.045` | Verificado 1:1 |
| 8 | Champi Velásquez, J. M. (2023) | Cap. I (1.1), Cap. II (2.2), Cap. III (3.1.2.1, Fig. 6, 3.2.1) | `http://hdl.handle.net/20.500.12872/844` | Verificado 1:1 |
| 9 | Chekol, A., Ketema, H., Endalew, B., y Asmare, G. (2023) | Cap. I (1.1), Cap. III (3.1.2.4, Fig. 8, Tabla 1, 3.2.5), Cap. VI | `https://doi.org/10.3389/frhs.2023.1059611` | Verificado 1:1 |
| 10 | Cohen, J. (1988) | Cap. IV (4.13) | Libro canónico (2.ª ed., Erlbaum) | Verificado 1:1 |
| 11 | Cohn, M. (2004) | Cap. III (3.1.1.3, 3.2.10, 3.3.1) | Libro canónico (Addison-Wesley) | Verificado 1:1 |
| 12 | Dang, T. T. T. et al. (2024) | Cap. I (1.1), Cap. II (2.1), Cap. III (3.1.2.3, Tabla 1, 3.2.15), Cap. VI | `https://doi.org/10.2196/45070` | Verificado 1:1 |
| 13 | Davis, F. D. (1989) | Cap. I (1.3.1), Cap. III (3.1.2.5, Tabla 1, 3.2.14), Cap. IV (4.9.2, 4.10.1), Cap. V (5.1.3), Cap. VI | `https://doi.org/10.2307/249008` | Verificado 1:1 |
| 14 | De la Torre Llorente, C. et al. (2010) | Cap. III (3.1.1.1, 3.2.16) | Libro técnico (1.ª ed., Krasis Press) | Verificado 1:1 |
| 15 | Dolan, S. B. et al. (2020) | Cap. VI (Discusión) | `https://doi.org/10.1186/s43058-020-00022-8` | Verificado 1:1 |
| 16 | Ergetie, F. S., Kassaw, A. T., y Sendekie, A. K. (2023) | Cap. I (1.1), Cap. II (2.1) | `https://doi.org/10.3389/fpubh.2023.1194807` | Verificado 1:1 |
| 17 | Garcia Villacorta, M. D. M., y Calderón Huaman, J. L. O. (2023) | Cap. I (1.1), Cap. II (2.2), Cap. III (3.1.2.1, 3.2.3, 3.2.12), Cap. VI | `https://hdl.handle.net/11537/33833` | Verificado 1:1 |
| 18 | Hernández-Sampieri, R., Fernández-Collado, C., y Baptista-Lucio, P. (2014) | Cap. I (1.3.3), Cap. IV (4.1 a 4.7, 4.10.1, 4.11, 4.12) | Libro canónico (6.ª ed., McGraw-Hill) | Verificado 1:1 |
| 19 | International Organization for Standardization, y International Electrotechnical Commission (2023) | Preliminares, Cap. I (1.3.1, 1.5), Cap. III (3.1.1.4, 3.3.5), Cap. IV (4.1, 4.9.1), Cap. VI | `https://www.iso.org/standard/78176.html` | Verificado 1:1 |
| 20 | Kigenza, R., Nsengiyumva, E., y Sabagirirwa, V. (2023) | Cap. I (1.1), Cap. II (2.1), Cap. III (3.1.2.2), Cap. VI | `https://doi.org/10.9745/GHSP-D-22-00295` | Verificado 1:1 |
| 21 | Luján Mora, S. (2002) | Cap. III (3.1.1.1, Fig. 1) | Libro técnico (Editorial Club Universitario) | Verificado 1:1 |
| 22 | Luo, J. et al. (2024) | Cap. III (3.1.2.5, Fig. 9, 3.2.14), Cap. VI | `https://doi.org/10.1057/s41599-024-02976-9` | Verificado 1:1 |
| 23 | Mego Navarro, D. P. (2021) | Cap. I (1.1), Cap. II (2.2), Cap. III (3.1.1.2, 3.2.12) | `https://hdl.handle.net/20.500.12867/5068` | Verificado 1:1 |
| 24 | Mekonen, Z. T., Cho, D. J., Nadeem, S. P., Garza-Reyes, J. A., y Fenta, T. G. (2024) | Cap. I (1.1), Cap. III (3.1.2.4, 3.2.4), Cap. VI | `https://doi.org/10.4258/hir.2024.30.4.375` | Verificado 1:1 |
| 25 | Ministerio de Salud (2022) | Cap. I (1.1), Cap. III (3.1.2.1, 3.2.1, 3.2.2, 3.2.9, 3.2.13), Cap. IV (4.9.2), Cap. VI | NTS N.° 196-MINSA/DGIESP-2022 (RM 884-2022) | Verificado 1:1 |
| 26 | Moumane, K. et al. (2024) | Cap. III (3.1.1.4, Fig. 5, 3.3.5), Cap. VI | `https://doi.org/10.31083/j.ceog5104088` | Verificado 1:1 |
| 27 | Ndlovu, K. et al. (2021) | Cap. III (3.1.2.5), Cap. VI | `https://doi.org/10.2196/32722` | Verificado 1:1 |
| 28 | Oliveira, V. C. D. et al. (2020) | Cap. III (3.1.2.5, Fig. 10), Cap. VI | `https://doi.org/10.1590/1518-8345.3360.3307` | Verificado 1:1 |
| 29 | Organización Panamericana de la Salud, y PATH (2020) | Cap. I (1.1), Cap. III (3.1.2.2, 3.2.17) | `https://iris.paho.org/handle/10665.2/53120` | Verificado 1:1 |
| 30 | Pressman, R. S. (2010) | Cap. III (3.1.1.3, Fig. 4, 3.2.8) | Libro canónico (7.ª ed., McGraw-Hill) | Verificado 1:1 |
| 31 | Ruiz Barea, R. (2023) | Cap. III (3.1.1.2, 3.2.6, 3.2.11) | Monografía académica (UOC) | Verificado 1:1 |
| 32 | Shen, J. et al. (2024) | Cap. I (1.1), Cap. II (2.1), Cap. III (3.1.2.2, 3.2.7, 3.2.18), Cap. VI | `https://doi.org/10.3389/fphar.2024.1373642` | Verificado 1:1 |
| 33 | Sommerville, I. (2016) | Cap. III (3.1.1.1, 3.1.1.2, Fig. 2, 3.1.1.3) | Libro canónico (10.ª ed., Pearson) | Verificado 1:1 |
| 34 | Tristán-López, A. (2008) | Cap. I (1.3.3), Cap. IV (4.12), Cap. VI (Anexo 4) | *Avances en Medición*, *6*(1), 37–48 | Verificado 1:1 |
| 35 | Wasswa, J. et al. (2023) | Cap. I (1.1), Cap. II (2.1), Cap. III (3.1.2.2, Fig. 7, 3.2.4, 3.2.17), Cap. VI | `https://doi.org/10.1186/s40545-023-00517-4` | Verificado 1:1 |
| 36 | World Health Organization (2021) | Cap. I (1.1), Cap. III (3.1.2.1), Cap. VI | `https://apps.who.int/iris/handle/10665/344249` | Verificado 1:1 |

---

## 3. Verificación Capitular y de Reglas Canónicas (`01_seguridad` a `04_protocolo_agentes`)

1. **Sección 1 — Páginas Preliminares (`scripts/utilidades/secciones_preliminares.py`):**
   - Portada, Carátula, Declaración Jurada, Dedicatoria, Agradecimientos, Resumen, Abstract, Chumasqa, Índice de Contenido, Índice de Tablas (Tablas 1 a 18) e Índice de Figuras (Figuras 1 a 19).
   - Paginación en números romanos en minúscula (`i, ii, iii...`) con `different_first_page_header_footer = True` para omitir numeración en la portada.
2. **Introducción y Capítulo I (`scripts/compiladores/capitulo1_builder.py`):**
   - `INTRODUCCIÓN` estructurada en 5 párrafos densos sin subtítulos internos.
   - `CAPÍTULO I: PROBLEMA DE INVESTIGACIÓN` con inicio directo en `1.1. Descripción de la realidad problemática`, seguido de `1.2. Formulación del problema`, `1.3. Justificación de la investigación` (teórica, práctica, metodológica, social y tecnológica), `1.4. Objetivos de la investigación` y `1.5. Limitaciones de la investigación`. Redactado íntegramente en tiempo pasado.
3. **Capítulo II (`scripts/compiladores/capitulo2_builder.py`):**
   - Inicio directo en `2.1. Antecedentes internacionales` (6 estudios: Shen et al., 2024; Dang et al., 2024; Kigenza et al., 2023; Balón Morejón, 2023; Ergetie et al., 2023; Wasswa et al., 2023) y `2.2. Antecedentes nacionales` (4 estudios: Astuhuaman Perez y Baltazar Maza, 2024; Mego Navarro, 2021; Garcia Villacorta y Calderón Huaman, 2023; Champi Velásquez, 2023).
4. **Capítulo III (`scripts/compiladores/capitulo3_builder.py`):**
   - Inicio directo en `3.1. Bases teóricas` (con Figuras 1 a 10 extraídas de fuentes primarias con nota adaptada y Tabla 1), `3.2. Marco conceptual` (18 definiciones numeradas `3.2.1` a `3.2.18` con citas APA 7) y `3.3. Metodología de desarrollo de software Extreme Programming (XP)` (Tablas 2 a 8 y Figuras 11 a 19 trazadas al código real de `syncova`).
5. **Capítulo IV (`scripts/compiladores/capitulo4_builder.py`):**
   - Inicio directo en `4.1. Tipo de investigación` hasta `4.13. Técnicas estadísticas para el procesamiento de la información` (13 secciones alineadas 1:1 con el modelo EPIS-UNAJMA).
   - Incluye las Tablas 9, 10, 11 y 12 sin fórmulas matemáticas ni signos `$` en celdas, y 12 ecuaciones OMML nativas (`<m:oMath>`) centradas en el cuerpo narrativo.
   - Confiabilidad del Instrumento N.° 03 con marcador formal `[Pendiente de cálculo tras levantamiento de campo]` (cero invención de Alfa de Cronbach).
6. **Capítulo V (`scripts/compiladores/capitulo5_builder.py`):**
   - Inicio directo en `5.1. Análisis descriptivo` (`5.1.1` a `5.1.3`) y `5.2. Análisis inferencial` (`5.2.1` y `5.2.2` con `5.2.2.1` a `5.2.2.4`).
   - Tablas 13, 14, 15, 16 y 17 estructuradas para la muestra censal ($N = n = 14$) con marcadores formales `[Pendiente]` en estricto cumplimiento de la Regla Canónica 01.
7. **Capítulo VI, Conclusiones, Recomendaciones, Referencias y Anexos (`scripts/compiladores/capitulo6_builder.py`):**
   - `CAPÍTULO VI: DISCUSIÓN` redactado en 4 bloques argumentativos en prosa corrida (Objetivo General y Objetivos Específicos 1, 2 y 3) con datos empíricos verificados de Mekonen et al. (2024) ($N = 102$, $\beta = 0.305$, $p = 0.008$; $\beta = -0.300$, $p = 0.032$; $R^2 = 0.533$).
   - 4 Conclusiones y 4 Recomendaciones en correspondencia 1:1 con los objetivos del estudio.
   - 36 Referencias Bibliográficas en APA 7 español con sangría francesa de 1.27 cm (`720 dxa`).
   - Anexos 1 a 5, incluyendo la Tabla 18 (*Matriz de consistencia de la investigación*) con texto formal limpio y sin exposición de rutas locales.

---

## 4. Verificación del Expediente de Validación e Instrumentos Oficiales (`salidas/instrumentos/`)

| N.° | Artefacto | Ruta | Estado |
|---|---|---|---|
| 1 | Expediente Integral de Validación por Juicio de Expertos | `salidas/instrumentos/EXPEDIENTE_VALIDACION_JUICIO_EXPERTOS_SIVAC.docx` | Verificado |
| 2 | Instrumento N.° 01: Ficha de Observación de Tiempos Cronometrados | `salidas/instrumentos/INSTRUMENTO_01_FICHA_TIEMPOS.docx` | Verificado |
| 3 | Instrumento N.° 02: Guía de Cotejo de Consistencia Documental | `salidas/instrumentos/INSTRUMENTO_02_GUIA_COTEJO.docx` | Verificado |
| 4 | Instrumento N.° 03: Cuestionario de Satisfacción del Usuario (TAM) | `salidas/instrumentos/INSTRUMENTO_03_CUESTIONARIO_TAM.docx` | Verificado |
| 5 | Matriz Automatizada de Cálculo de IVC y V de Aiken | `salidas/instrumentos/MATRIZ_CALCULO_IVC_AIKEN_SIVAC.xlsx` | Verificado |
